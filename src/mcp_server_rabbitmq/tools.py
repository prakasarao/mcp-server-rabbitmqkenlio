from .models import (
    Enqueue, 
    Fanout, 
    ListQueues, 
    ListExchanges, 
    GetQueueInfo, 
    DeleteQueue,
    PurgeQueue,
    DeleteExchange,
    GetExchangeInfo
)
from mcp.types import (
    Tool,
)

MCP_TOOLS = [
    Tool(
        name="enqueue",
        description="""Enqueue a message to a queue hosted on RabbitMQ""",
        inputSchema=Enqueue.model_json_schema(),
    ),
    Tool(
        name="fanout",
        description="""Publish a message to an exchange with fanout type""",
        inputSchema=Fanout.model_json_schema(),
    ),
    Tool(
        name="list_queues",
        description="""List all the queues in the broker""",
        inputSchema=ListQueues.model_json_schema(),
    ),
    Tool(
        name="list_exchanges",
        description="""List all the exchanges in the broker""",
        inputSchema=ListExchanges.model_json_schema(),
    ),
    Tool(
        name="get_queue_info",
        description="""Get detailed information about a specific queue""",
        inputSchema=GetQueueInfo.model_json_schema(),
    ),
    Tool(
        name="delete_queue",
        description="""Delete a specific queue""",
        inputSchema=DeleteQueue.model_json_schema(),
    ),
    Tool(
        name="purge_queue",
        description="""Remove all messages from a specific queue""",
        inputSchema=PurgeQueue.model_json_schema(),
    ),
    Tool(
        name="delete_exchange",
        description="""Delete a specific exchange""",
        inputSchema=DeleteExchange.model_json_schema(),
    ),
    Tool(
        name="get_exchange_info",
        description="""Get detailed information about a specific exchange""",
        inputSchema=GetExchangeInfo.model_json_schema(),
    )
]

MCP_TOOL_ROUTING = {
    
}