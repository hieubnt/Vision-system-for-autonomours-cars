from abc import ABC
from threading import Thread, Lock
from typing import Literal

from pydantic import validate_call, BaseModel, ConfigDict, conset

from logger import Logger
from utils.base_config import BaseConfig
from .pub_sub_hub import PubSubHub
from .topics import BaseTopic, TopicCreator

class PublisherConfig(BaseConfig):
    pub_name: str
    pub_topics: conset(str, min_length=1)

class Publisher(ABC, BaseModel):
    """
    class to store Handlers, which is only have one instance according to one class.
    Support hardcoding using tuple.
    """

    model_config = ConfigDict(validate_default=True, frozen=True)
    pub_topics: conset(str, min_length=1)
    pub_name: str

    _config: PublisherConfig

    @validate_call()
    def __init__(self,*, pub_config: PublisherConfig):
        self._config = pub_config
        super().__init__(**self._extract_pub_config())

        self._lock = Lock()

        self._push_to_hub()

    def _extract_pub_config(self)->dict:
        pub_config = dict(
            pub_name=self._config.pub_name,
            pub_topics=self._config.pub_topics
        )
        return pub_config

    def _push_to_hub(self):
        """
        Assign topics to pub_sub_hub, topic should be predefined by inheriting BaseTopic.
        Storage and Hub will check if Publisher is valid to publish.
        """
        PubSubHub().add_publisher(self)
        Logger().log(f"Topics {self.pub_topics} has been released successfully.",
                     log_name=f"Publisher \'{self.pub_name}\'")

    @validate_call
    def publish(self, *,
                topic: str,
                data: dict,
                mode: Literal['sync', 'async'] = 'async',
                lock: bool = False
                ):
        """
        Create Topic from data and publish it.

        :param topic: topic to publish, raise error if Publisher or System not support
        :param data:
        :param mode:
        :param lock:
        :return:
        """

        if mode == 'sync':
            self._publish(topic=topic, data=data)
        if mode == 'async':
            if lock:
                self._lock.acquire()
                thread = Thread(target=self._publish, kwargs={'topics': topic, 'data': data})
                thread.start()

    def _publish(self, *,
                 topic: str,
                 data: dict):
        ready_topic = self._create_topic_from_dict(topic, data)
        PubSubHub().publish(ready_topic)
        if self._lock.locked():
            self._lock.release()

    def _create_topic_from_dict(self, topic_name: str, data: dict) -> BaseTopic:
        if topic_name not in self.pub_topics:
            except_mess = f'Publisher \'{self.pub_name}\' does not support topic \'{topic_name}\'.'
            self._raise(except_mess)
        try:
            return TopicCreator.create(topic_name=topic_name, data=data)
        except Exception:
            self._raise(f'System does not support Topic name \'{topic_name}\'')

    def _raise(self, message: str):
        Logger().log(f"Raise Exception: \"{message}\"", log_name=f"Publisher \'{self.pub_name}\'", )
        raise Exception(message)
