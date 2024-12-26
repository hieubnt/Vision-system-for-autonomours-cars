from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing import Literal, Union
from abc import ABC, abstractmethod
from ..topics import BaseTopic
from queue import Queue, LifoQueue

#Message queue
class BaseMessageQueue(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)

    queue_type: str
    queue_size: int
    drop_first: bool

    @abstractmethod
    def push(self, topic: BaseTopic) -> None:
        pass

    @abstractmethod
    def pop(self) -> BaseTopic:
        pass

    @abstractmethod
    def get(self) -> BaseTopic:
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass

class FIFOQueue(BaseMessageQueue):
    queue_type: Literal['FIFO']

    def push(self, topic: BaseTopic) -> None:
        pass

    def pop(self) -> BaseTopic:
        pass


class LIFOQueue(BaseMessageQueue):
    queue_type: Literal['LIFO']
    def push(self, topic: BaseTopic) -> None:
        pass

    def pop(self) -> BaseTopic:
        pass

QueueType = Union[FIFOQueue,LIFOQueue]

class MessageQueueCreator(BaseModel):
    queue: QueueType = Field(...,discriminator='queue_type')

    @classmethod
    @validate_call
    def create(cls,queue_type:str, queue_size:int, drop_first:bool):

