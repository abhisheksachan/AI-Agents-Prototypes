import asyncio
import os
import sys
import json
from dotenv import load_dotenv

# MCP Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Gemini Imports
from google import genai
from google.genai import types

load_dotenv()

# We need to run the server script from Prototype 04
SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "04_mcp", "server.py")

async def run_agent():
    print("--- 05 Gemini + MCP Bridge Demo ---")
    
    # 1. Initialize Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found.")
        return
    
    # Note: Using the sync client but we'll call it carefully, 
    # or we can use the async patterns if needed. 
    # The google-genai SDK 1.x is primarily sync.
    gemini_client = genai.Client(api_key=gemini_api_key)
    MODEL_ID = "gemini-flash-latest"

    # 2. Connect to MCP Server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT],
        env=None
    )

    print(f"Connecting to MCP Server at {SERVER_SCRIPT}...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as mcp_session:
            # Initialize MCP
            await mcp_session.initialize()
            
            # List tools from MCP
            mcp_tools = await mcp_session.list_tools()
            print(f"MCP Server connected. Found {len(mcp_tools.tools)} tools.")

            # --- BRIDGE LOGIC ---
            # We want Gemini to use these tools. 
            # In a real system, we'd dynamically convert MCP tool schemas to Gemini tool schemas.
            # For this demo, we'll manually bridge 'add_note'.
            
            async def call_mcp_tool(name, args):
                print(f"DEBUG: Redirecting tool call '{name}' to MCP Server...")
                result = await mcp_session.call_tool(name, arguments=args)
                return result.content[0].text

            # Gemini doesn't know how to "await" internally in its auto-loop.
            # So we'll use a manual ReAct loop for the MCP bridge.
            
            messages = [{"role": "user", "content": "Keep a note that I need to learn about MCP Agents today."}]
            print(f"\nUser: {messages[0]['content']}")

            # Define the tool for Gemini (Manually matching the MCP server's add_note)
            # The google-genai SDK expects tools to be a list of Tool objects,
            # which contain a list of function_declarations.
            gemini_tools = [
                types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(
                            name="add_note",
                            description="Add a new note to the list.",
                            parameters=types.Schema(
                                type="OBJECT",
                                properties={
                                    "content": types.Schema(
                                        type="STRING", 
                                        description="The text of the note"
                                    )
                                },
                                required=["content"]
                            )
                        )
                    ]
                )
            ]

            # We use the generate_content call
            response = gemini_client.models.generate_content(
                model=MODEL_ID,
                contents=messages[0]['content'],
                config=types.GenerateContentConfig(
                    tools=gemini_tools,
                )
            )

            # Check for tool call
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        func_name = part.function_call.name
                        func_args = part.function_call.args
                        
                        print(f"Gemini wants to call: {func_name} with {func_args}")
                        
                        # Execute via MCP
                        mcp_result = await call_mcp_tool(func_name, func_args)
                        print(f"MCP Result: {mcp_result}")
                        
                        # Feed back to Gemini for final answer
                        # We hand the result back as a model turn (the feedback)
                        # The SDK expects a specific format if we aren't using ChatSession.
                        final_response = gemini_client.models.generate_content(
                            model=MODEL_ID,
                            contents=[
                                types.Content(role="user", parts=[types.Part(text=messages[0]['content'])]),
                                response.candidates[0].content, # The function call (role: model)
                                types.Content(role="user", parts=[types.Part(text=f"Observation from tool: {mcp_result}")])
                            ]
                        )
                        print(f"\nFinal Answer: {final_response.text}")
            else:
                print(f"AI: {response.text}")

if __name__ == "__main__":
    asyncio.run(run_agent())
