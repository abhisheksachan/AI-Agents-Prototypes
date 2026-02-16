import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    # Define how to connect to our server
    server_params = StdioServerParameters(
        command=sys.executable,  # Run with the same python interpreter
        args=["server.py"],      # The server script
        env=None                 # Inherit environment
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # 1. List available tools
            tools = await session.list_tools()
            print(f"Server provides {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f" - {tool.name}: {tool.description}")

            # 2. List available resources
            resources = await session.list_resources()
            print(f"\nServer provides {len(resources.resources)} resources:")
            for resource in resources.resources:
                print(f" - {resource.uri}: {resource.name}")

            # 3. Call a tool
            print("\nCalling tool 'add_note'...")
            result = await session.call_tool("add_note", arguments={"content": "Buying milk"})
            print(f"Tool Result: {result.content[0].text}")

            print("\nCalling tool 'add_note' again...")
            await session.call_tool("add_note", arguments={"content": "Walking the dog"})

            # 4. Read a resource
            print("\nReading resource 'note://list'...")
            # Note: In real MCP, you read a resource by URI template or direct URI
            # Our simple server might not implement 'read_resource' perfectly unless we defined it. 
            # But let's try (FastMCP handles this usually).
            try:
                content = await session.read_resource("note://list")
                print(f"Resource Content:\n{content.contents[0].text}")
            except Exception as e:
                print(f"Could not read resource: {e}")

            # 5. List prompts
            prompts = await session.list_prompts()
            print(f"\nServer provides {len(prompts.prompts)} prompts:")
            for prompt in prompts.prompts:
                print(f" - {prompt.name}")

            # 6. Get a prompt
            print("\nGetting prompt 'summarize_notes'...")
            prompt_result = await session.get_prompt("summarize_notes")
            print(f"Prompt Content:\n{prompt_result.messages[0].content.text}")

if __name__ == "__main__":
    # Ensure we run in the right directory or adjust args
    # For this demo, run this script from the 04_mcp directory!
    asyncio.run(run())
