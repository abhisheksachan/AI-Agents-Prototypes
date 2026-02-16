from mcp.server.fastmcp import FastMCP

# Create an MCP server named "Notes App"
mcp = FastMCP("Notes App")

# Global state to simulate a database
notes = []

@mcp.resource("note://list")
def list_notes() -> str:
    """Return a list of all notes."""
    return "\n".join(f"- {note}" for note in notes)

@mcp.tool()
def add_note(content: str) -> str:
    """Add a new note to the list."""
    notes.append(content)
    return f"Added note: {content}"

@mcp.prompt()
def summarize_notes() -> str:
    """Create a prompt to summarize all notes."""
    return f"Here are the user's notes:\n{list_notes()}\n\nPlease summarize them."

if __name__ == "__main__":
    # Run the server
    mcp.run()
