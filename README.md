# Gemini AI Agents Prototypes

This repository contains a progressive set of prototypes for learning about AI Agents using the **Google Gemini API**, ranging from basic scripts to advanced multi-agent orchestration with **LangChain** and **LangGraph**.

## 🚀 Prototypes

### 1. Basic Interaction (`01_basic_interaction.py`)
- Send a prompt and get a text response.
- Learn about system instructions and the basic API loop.

### 2. Tool Use / Function Calling (`02_tool_calling.py`)
- Demonstrates how Gemini can call your Python functions.
- **Key Concepts**: Function reflection and automatic tool execution loop.

### 3. ReAct Agent (`03_react_agent.py`)
- A primitive agent that uses multiple tools in sequence to solve a complex goal.
- **Key Concepts**: Logic loops and reasoning-action cycles.

### 4. Model Context Protocol (MCP) (`04_mcp/` & `05_gemini_bridge.py`)
- Standardizes tool connection using the Model Context Protocol.
- Includes a bridge script to connect the Gemini SDK to an MCP server.

### 5. LangChain Orchestration (`06_langchain_agent.py`)
- Moving from manual loops to a framework.
- Uses **LangChain v1.x** to orchestrate tool-calling agents with standardized tool definitions.

### 6. Multi-Agent Team (`07_multi_agent.py`)
- A static workflow using **LangGraph**.
- Features a **Researcher** and a **Writer** working in a fixed pipeline (Researcher → Writer).

### 7. Dynamic Multi-Agent Workflow (`08_dynamic_multi_agent.py`)
- Advanced orchestration using **Conditional Routing**.
- Agents act as "Specialists" that decide when to hand off tasks to each other based on conversation state.
- **Key Concepts**: StateGraph, Conditional Edges, and Supervisor Routing.

---

## 🛠 Setup

1. **Get an API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Environment Configuration**: 
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to the .env file
   ```
3. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install langchain langchain-google-genai langchain-community langgraph
   ```

## 🏃 Running

Recommended model for latest prototypes: `gemini-2.5-flash` (higher rate limits).

```bash
# Basic examples
python 01_basic_interaction.py
python 02_tool_calling.py

# Multi-agent examples
python 07_multi_agent.py
python 08_dynamic_multi_agent.py
```

## 🧠 Technologies Used
- **Google GenAI Python SDK**: Direct interaction with Gemini.
- **LangChain**: High-level agent orchestration.
- **LangGraph**: building stateful, multi-agent workflows.
- **MCP**: Standardizing external tool access.
