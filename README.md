# Gemini AI Agents Prototypes

This repository contains simplified prototypes for learning about AI Agents using the **Google Gemini API**.

## Prototypes

1. **Basic Interaction** (`01_basic_interaction.py`)
   - Send a prompt and get a text response.
   - Learn about system instructions and the basic API loop.

2. **Tool Use / Function Calling** (`02_tool_calling.py`)
   - How Gemini can call your Python functions.
   - **Concepts**: Function reflection (no JSON schema needed) and automatic execution.

3. **ReAct Agent** (`03_react_agent.py`)
   - An agent that uses multiple tools in sequence to solve a complex goal.
   - **Concepts**: Multi-turn chat sessions and reasoning loops.

4. **Model Context Protocol (MCP)** (`04_mcp/`)
   - Connecting your tools to a standardized protocol.

## Setup

1. **Get an API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Create .env**: 
   ```bash
   cp .env.example .env
   # Add your key to the file
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running

```bash
python 01_basic_interaction.py
python 02_tool_calling.py
python 03_react_agent.py
```
