from typing import Annotated
from pydantic import BaseModel, Field

class Enqueue(BaseModel):
    message: Annotated[str, Field(description="The message to publish")]
    queue: Annotated[str, Field(description="The name of the queue")]

class Fanout(BaseModel):
    message: Annotated[str, Field(description="The message to publish")]
    exchange: Annotated[str, Field(description="The name of the exchange")]

class ListQueues(BaseModel):
    pass

class ListExchanges(BaseModel):
    pass

class GetQueueInfo(BaseModel):
    queue: Annotated[str, Field(description="The name of the queue to get info about")]
    vhost: Annotated[str, Field(description="The virtual host where the queue exists")] = "/"

class DeleteQueue(BaseModel):
    queue: Annotated[str, Field(description="The name of the queue to delete")]
    vhost: Annotated[str, Field(description="The virtual host where the queue exists")] = "/"

class PurgeQueue(BaseModel):
    queue: Annotated[str, Field(description="The name of the queue to purge")]
    vhost: Annotated[str, Field(description="The virtual host where the queue exists")] = "/"

class DeleteExchange(BaseModel):
    exchange: Annotated[str, Field(description="The name of the exchange to delete")]
    vhost: Annotated[str, Field(description="The virtual host where the exchange exists")] = "/"

class GetExchangeInfo(BaseModel):
    exchange: Annotated[str, Field(description="The name of the exchange to get info about")]
    vhost: Annotated[str, Field(description="The virtual host where the exchange exists")] = "/"
