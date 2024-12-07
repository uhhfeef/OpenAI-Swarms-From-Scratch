from pydantic import BaseModel
from openai import OpenAI
import json
import inspect

client = OpenAI(api_key=api_key)

class Agent(BaseModel):
    name: str
    instructions: str
    functions: list = []
  
    
def process_refund(item_id, reason="NOT SPECIFIED"):
    """Refund an item. Refund an item. Make sure you have the item_id of the form item_... Ask for user confirmation before processing the refund."""
    print(f"[mock] Refunding item {item_id} because {reason}...")
    return "Success!"

def apply_discount():
    """Apply a discount to the user's cart."""
    print("[mock] Applying discount...")
    return "Applied discount of 11%"

def transfer_back_to_triage():
    """Call this function if a user is asking about a topic that is not handled by the current agent."""
    print("Transferring back to Triage Agent...")
    return triage_agent

def transfer_to_sales():
    print("Transferring to Sales Agent...")
    return sales_agent

def transfer_to_refunds():
    print("Transferring to Refunds Agent...")
    return refunds_agent

triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which agent is best suited to handle the user's request, and transfer the conversation to that agent. Refunds agent handles discounts.",
    functions=[transfer_to_sales, transfer_to_refunds],
)
sales_agent = Agent(
    name="Sales Agent",
    instructions="Be super enthusiastic about selling bees.",
    functions=[transfer_back_to_triage],
)
refunds_agent = Agent(
    name="Refunds Agent",
    instructions="Help the user with a refund. If the reason is that it was too expensive, offer the user a refund code. If they insist, then process the refund.",
    functions=[process_refund, apply_discount, transfer_back_to_triage],
)    

def func_to_json(func):
    signature = inspect.signature(func)
    props = {param.name: {"type": "string"} for param in signature.parameters.values()}
    required = [param.name for param in signature.parameters.values() if param.default == inspect._empty]

    # print(required)
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": props or {},
                "required": required or [],
            },
        },
    }

def handle_function_result(function_result):
    match function_result:
        case Agent() as agent:
            print(f"Agent: {agent.name}")
            
            return {
                "agent": agent
            }
        
        case _:
            return {
                "value": str(function_result)
            }

def get_chat_completion(agent, messages):
    tools = [func_to_json(f) for f in agent.functions]
    total_messages = [{"role": "system", "content": agent.instructions }] + messages
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=total_messages,
        tools=tools,
    )
    return completion

def run(agent):
    messages = []
    active_agent = agent
    while True:
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})
        
        while True:
            completion = get_chat_completion(active_agent, messages)
            message = completion.choices[0].message
            # since we have only one function, we can hardcode function_map for now
            function_map = {func.__name__: func for func in active_agent.functions}
            
            if message.tool_calls:
                # OpenAI needs context that a tool was called, so we append it to the messages
                messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})

                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    function = function_map[tool_name]
                    
                    args = json.loads(tool_call.function.arguments)
                    
                    function_result = function(**args)  
                    
                    if function_result:
                        result = handle_function_result(function_result)
                        if "agent" in result:
                            active_agent = result["agent"]
                    
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(function_result)})
                    
            else:
                # If there are no tool_calls, exit and stop looping
                response = completion.choices[0].message.content

                break
        
        print(f"\033[94m{active_agent.name}\033[0m:", end=" ")
        print(response)

if __name__ == "__main__":    
    run(triage_agent)
