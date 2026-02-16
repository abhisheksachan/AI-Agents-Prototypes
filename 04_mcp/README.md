# MCP Demo (Model Context Protocol)

This directory demonstrates how to build an MCP server and connect to it with a client.

## Setup

1. Make sure you have the `mcp[cli]` package installed:
   ```bash
   pip install "mcp[cli]"
   ```

2. This demo uses `FastMCP` which simplifies server creation.

## Running the Demo

1. **Run the Server Manually (Optional)**:
   You can verify the server works by running:
   ```bash
   python server.py
   ```
   It will start and wait for JSON-RPC messages on stdin (it will look like it's hanging, that's normal!).

2. **Run the Client**:
   The client script will automatically start the server as a subprocess and talk to it.
   ```bash
   python client_demo.py
   ```
   You should see the client listing tools, calling `add_note`, and reading the `note://list` resource.

## How it Works

- **server.py**: Uses `FastMCP` to expose python functions as tools and prompts.
- **client_demo.py**: Uses the `mcp` client library to connect to the server over stdio.

## Connecting to Claude Desktop

If you have the Claude Desktop app, you can add this server to your configuration:

1. Open Claude Desktop strict configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this entry:
   ```json
   {
     "mcpServers": {
       "my-notes-app": {
         "command": "python",
         "args": ["/absolute/path/to/AI Agents/04_mcp/server.py"]
       }
     }
   }
   ```
   (Replace `/absolute/path/to/...` with your actual full path)

3. Restart Claude Desktop. You will see a hammered icon and be able to ask Claude to "Add a note" or "Summarize my notes".
