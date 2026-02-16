from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

# Create a server instance
app = Server("simple-notes")

notes = []

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_note",
            description="Add a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="list_notes",
            description="List all notes",
            inputSchema={"type": "object"}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_note":
        content = arguments["content"]
        notes.append(content)
        return [TextContent(type="text", text=f"Added note: {content}")]
    elif name == "list_notes":
        return [TextContent(type="text", text="\n".join(notes))]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
