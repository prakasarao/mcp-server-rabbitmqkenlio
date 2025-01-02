from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
import pika
import ssl
from .models import Enqueue
from .logger import Logger, LOG_LEVEL


async def serve(rabbitmq_host: str, port: int, username: str, password: str, use_tls: bool, logging_level: LOG_LEVEL = LOG_LEVEL.WARNING) -> None:
    # Setup server and logger
    server = Server("mcp-rabbitmq")
    # Make logger another option to pass
    logger = Logger("server.log")
    # Setup RabbitMQ connection metadata
    protocol = "amqps" if use_tls else "amqp"
    url = f"{protocol}://{username}:{password}@{rabbitmq_host}:{port}"
    parameters = pika.URLParameters(url)
    if use_tls:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="enqueue",
                description="""Enqueue a message to a queue hosted on RabbitMQ""",
                inputSchema=Enqueue.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str,
        arguments: dict
    ) -> list[TextContent]:
        if name == "enqueue":
            message = arguments["message"]
            queue = arguments["queue"]
            # Send to RabbitMQ host
            try:
                connection = pika.BlockingConnection(parameters)
                channel = connection.channel()
                channel.queue_declare(queue)
                channel.basic_publish(exchange="", routing_key=queue, body=message)
                return [TextContent(type="text", text=str("suceeded"))]
            except Exception as e:
                logger.error(f"[ERROR] {e}")
                return [TextContent(type="text", text=str("failed"))]
        raise ValueError(f"Tool not found: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
