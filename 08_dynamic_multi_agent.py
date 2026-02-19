import os
from typing import Annotated, Sequence, TypedDict, Literal
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Shared State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# 2. Setup Model
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# 3. Decision Router
def supervisor_router(state: AgentState) -> Literal["researcher", "writer", "__end__"]:
    last_message = state["messages"][-1]
    content = last_message.content.upper()
    
    if "RESEARCH_COMPLETE" in content:
        return "writer"
    if "NEED_MORE_RESEARCH" in content:
        return "researcher"
    
    # If it's a Human query, we always start with Research
    if isinstance(last_message, HumanMessage):
        return "researcher"
    
    return "__end__"

# 4. Pure Node Functions (Direct LLM Calls for maximum reliability)
def researcher_node(state: AgentState):
    print("\n[Node] Researcher is gathering facts...")
    system_prompt = (
        "You are a Research Specialist. List 3 key facts about the topic. "
        "End your message with RESEARCH_COMPLETE."
    )
    # Combine system prompt with conversation history
    messages = [AIMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=response.content, name="Researcher")]}

def writer_node(state: AgentState):
    print("\n[Node] Writer is crafting the response...")
    system_prompt = (
        "You are a Creative Writer. Turn the provided facts into a tiny 2-line rhyming poem. "
        "If there are no facts, say NEED_MORE_RESEARCH. Otherwise, just output the poem."
    )
    # The writer sees everything the researcher found
    messages = [AIMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(messages)
    return {"messages": [AIMessage(content=response.content, name="Writer")]}

# 5. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

workflow.add_conditional_edges(START, supervisor_router)
workflow.add_conditional_edges("researcher", supervisor_router)
workflow.add_conditional_edges("writer", supervisor_router)

multi_agent_system = workflow.compile()

if __name__ == "__main__":
    print("🚀 Dynamic Specialist Workflow (Reliable Version)")
    
    query = "Write a poem about the discovery of Electricity."
    inputs = {"messages": [HumanMessage(content=query)]}
    
    for chunk in multi_agent_system.stream(inputs, stream_mode="values"):
        if "messages" in chunk:
            msg = chunk["messages"][-1]
            if not isinstance(msg, HumanMessage):
                name = getattr(msg, "name", "Assistant")
                print(f"\n[{name.upper()}]:\n{msg.content}")

    print("\n" + "="*40)
    print("✅ Coordination Complete!")
