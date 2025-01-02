# RabbitMQ MCP Server

A [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) server implementation for RabbitMQ. Enabling MCP client to interact with queues and topics hosted in a RabbitMQ instance.

## Running locally with the Claude desktop app

1. Clone this repository.
2. Add the following to your `claude_desktop_config.json` file:
- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```
{
    "mcpServers": {
      "rabbitmq": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/repo/mcp-server-rabbitmq", 
            "run", 
            "mcp-server-rabbitmq",
            "--rabbitmq-host",
            "<hostname ex. test.rabbit.com, localhost>",
            "--port", 
            "<port number ex. 5672>",
            "--username",
            "<rabbitmq username>",
            "--password",
            "<rabbitmq password>",
            "--use-tls",
            "<true if uses amqps, false otherwise>"
        ]
      }
    }
}
```
4. Install and open the [Claude desktop app](https://claude.ai/download).
5. Try asking Claude to do a read/write operation of some sort to confirm the setup (e.g. ask it to publish a message to a queue). If there are issues, use the Debugging tools provided in the MCP documentation [here](https://modelcontextprotocol.io/docs/tools/debugging).
