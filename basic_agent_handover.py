from pydantic import BaseModel
from openai import OpenAI
import json

client = OpenAI(api_key=api_key)

class Agent(BaseModel):
    name: str
    instructions: str
    functions: list = []
    
# function to call
def transfer_to_spanish_agent():
    print("Tranferring to spanish agent...")
    return spanish_agent

english_agent = Agent(
    name="English Agent",
    instructions="You only speak English.",
    functions=[transfer_to_spanish_agent],
)

spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish.",
)


tools = [
    { 'type': 'function',
      'function': {
          'name': 'transfer_to_spanish_agent',
          'description': 'Transfer spanish speaking users immediately.',
          'parameters': {
              'type': 'object',
              'properties': {},
              'required': []
          }
      }
    }
]

def handle_function_result(function_result):
    match function_result:
        case Agent() as agent:
            print(f"Agent: {agent.name}")
            
            return agent
        case _:
            # This is the default case if the structure doesn't match
            print("Not a valid agent structure")
            return False

def get_chat_completion(agent, messages, tools):
    total_messages = [{"role": "system", "content": agent.instructions }] + messages
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=total_messages,
        tools=tools,
    )
    return completion


def run(agent, messages):
    active_agent = agent
    while True:
        completion = get_chat_completion(active_agent, messages, tools)
        message = completion.choices[0].message
        # since we have only one function, we can hardcode function_map for now
        function_map = {
            'transfer_to_spanish_agent': transfer_to_spanish_agent
        }
        
        if message.tool_calls:
            # OpenAI needs context that a tool was called, so we append it to the messages
            messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                function = function_map[tool_name]
                
                function_result = function()
                
                if function_result:
                    active_agent = handle_function_result(function_result)
                else:
                    print("Not a valid agent structure")
                
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(function_result)})
        else:
            # If there are no tool_calls, exit and stop looping
            print(completion.choices[0].message.content)

            break
        
if __name__ == "__main__":    
    messages = [{"role": "user", "content": "Hola. ¿Como estás?"}]
    run(english_agent, messages)
