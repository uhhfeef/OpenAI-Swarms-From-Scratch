# OpenAI Swarms From Scratch

This repository contains the example code from my Medium article [Building OpenAI Swarm from Scratch](https://uhhfeef.medium.com/building-openai-swarm-from-scratch-8a0e89352c75), where I break down the fundamentals of AI agents and demonstrate how to build them using OpenAI's framework.

## Overview

The examples in this repository showcase:
1. Building a basic AI agent from scratch
2. Understanding the core components of agents (prompts, tools, and functions)
3. Implementing multi-agent systems with language-specific agents
4. Demonstrating agent handoff and specialized behaviors

## Examples Included

### 1. Basic Weather Agent
A simple example showing how to create an agent that can:
- Accept weather-related queries
- Use function calling to get weather data
- Process and return weather information

### 2. Multi-Language Agents
A more advanced example demonstrating:
- English and Spanish language agents
- Agent handoff mechanisms
- System prompt-based behavior modification

## Getting Started

1. Clone this repository
2. Install the required dependencies:
```bash
pip install openai
```
3. Set up your OpenAI API key:
```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## Key Concepts Covered

- Function calling with OpenAI's API
- Tool definitions and implementations
- System prompts and agent behavior
- Message handling and conversation flows
- Multi-agent architectures

## Learn More

For a detailed explanation of these concepts and step-by-step guides, check out the full article on [Medium](https://uhhfeef.medium.com/building-openai-swarm-from-scratch-8a0e89352c75).

## Contributing

Feel free to submit issues and enhancement requests!

---
Created by [Afeef](https://uhhfeef.medium.com/)
