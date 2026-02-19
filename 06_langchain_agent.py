import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool

# 1. Load Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Define Tools
@tool
def get_system_time() -> str:
    """Returns the current system time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def process_data(text: str) -> str:
    """Processes text by converting it to uppercase and counting characters."""
    return f"Upper: {text.upper()} | Count: {len(text)}"

tools = [get_system_time, process_data]

# 3. Initialize Model
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=api_key)

# 4. Create the Agent
# Behind the scenes, LangChain creates a graph that manages the 'messages' list state.
agent = create_agent(model=llm, tools=tools)

if __name__ == "__main__":
    query = "What is the current time? Also, process 'Stitching is cool' for me."
    print(f"User: {query}\n" + "-"*30)

    # --- OPTION A: Streaming (Watching the stitching happen) ---
    print("\n[STEP-BY-STEP ORCHESTRATION]")
    inputs = {"messages": [{"role": "user", "content": query}]}
    
    for chunk in agent.stream(inputs, stream_mode="updates"):
        for node, output in chunk.items():
            # In create_agent, nodes are named 'model' (the brain) and 'tools' (the hands)
            if "messages" in output:
                msg = output["messages"][-1]
                if node == "model":
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        print(f"🤖 Brain: I need to use tools: {[tc['name'] for tc in msg.tool_calls]}")
                    if msg.content:
                        print(f"💬 Brain (Final Answer): {msg.content}")
                elif node == "tools":
                    print(f"🛠️ Hands: Tool execution finished. Result: {msg.content}")

    # --- OPTION B: Simple Invoke (Getting the final result directly) ---
    print("\n" + "-"*30)
    print("[SIMPLE INVOKE - THE FINAL RESULT]")
    
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    
    # The 'result' is the full final state of the graph.
    # The last message in the 'messages' list is the final stitched response.
    final_answer = result["messages"][-1].content
    print(f"Final Outcome: {final_answer}")
