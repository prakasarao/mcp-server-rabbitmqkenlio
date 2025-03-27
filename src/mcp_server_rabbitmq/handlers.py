from .connection import RabbitMQConnection
from .admin import RabbitMQAdmin
from typing import List

def handle_enqueue(rabbitmq: RabbitMQConnection, queue: str, message: str):
    connection, channel = rabbitmq.get_channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()

def handle_fanout(rabbitmq: RabbitMQConnection, exchange: str, message: str):
    connection, channel = rabbitmq.get_channel()
    channel.exchange_declare(exchange=exchange, exchange_type="fanout")
    channel.basic_publish(exchange=exchange, routing_key="", body=message)
    connection.close()

def handle_list_queues(rabbitmq_admin: RabbitMQAdmin) -> List[str]:
    result = rabbitmq_admin.list_queues()
    return [queue['name'] for queue in result]
