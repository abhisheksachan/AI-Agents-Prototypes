import os
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Setup State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2. Load Environment & Model
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# Testing 2.5-flash as it may have higher limits
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# 3. Node 1: The Researcher
def researcher_node(state: AgentState):
    print("\n--- [AGENT: RESEARCHER] ---")
    # Instead of calling the API twice (logic + tool), we simulate the research
    # and only call the API once to "think" about the summary.
    user_query = state["messages"][0].content
    research_data = "LangChain (founded 2022) is a framework to build LLM apps by chaining components like prompts, models, and memory."
    
    prompt = f"Summarize this research data for the query '{user_query}': {research_data}"
    response = llm.invoke(prompt)
    
    # We add the researcher's name to the message so we know who is talking
    return {"messages": [AIMessage(content=response.content, name="Researcher")]}

# 4. Node 2: The Writer
def writer_node(state: AgentState):
    print("\n--- [AGENT: WRITER] ---")
    # The writer sees the Researcher's summary in the 'messages' list
    research_summary = state["messages"][-1].content
    
    prompt = f"Based on this research: '{research_summary}', write a 1-line rhyming slogan."
    response = llm.invoke(prompt)
    
    return {"messages": [AIMessage(content=response.content, name="Writer")]}

# 5. Build the Workflow (The "Talking" logic)
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

multi_agent_system = workflow.compile()

if __name__ == "__main__":
    print("🚀 Starting Quota-Friendly Multi-Agent System...")
    
    query = "What is LangChain? I need a slogan for it."
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # Run the graph
    for chunk in multi_agent_system.stream(inputs, stream_mode="values"):
        if "messages" in chunk:
            msg = chunk["messages"][-1]
            if isinstance(msg, AIMessage):
                name = getattr(msg, "name", "Assistant")
                print(f"[{name}]: {msg.content}")

    print("\n" + "="*40)
    print("✅ Collaboration Complete!")
