from abc import ABC, abstractmethod
from threading import Lock, Thread

from logger import Logger
from utils.base_config import BaseConfig
from .pub_sub_hub.hub import PubSubHub
from pydantic import BaseModel, ConfigDict, conset, validate_call, Field
from .topics import BaseTopic


class SubscriberHandler(ABC, BaseModel):
    model_config = ConfigDict(frozen = True, validate_default= True)
    topic_name: str
    lock: Lock = Lock()



    @validate_call
    def handle(self,*, topic: BaseTopic, subscriber: 'Subscriber', **kwargs):
        if topic.topic_name != self.topic_name:
            self._raise(f"Topic name of input is mismatch with topic name of handler."
                        f" Got {topic.topic_name} but expect {self.topic_name}",
                        subscriber.sub_name)


        self._log(f"Topic \'{self.topic_name}\' is handling.",subscriber.sub_name)
        self._handle(topic = topic, subscriber = subscriber, **kwargs)
        self._log(f"Topic \'{self.topic_name}\' was handled successfully.",subscriber.sub_name)

    @abstractmethod
    def handle_impl(self,*,topic: BaseTopic,subscriber: 'Subscriber', **kwargs):
        pass



    def _raise(self, message: str, sub_name:str):
        Logger().log(f"Raise Exception: \"{message}\"",
                     log_name=f"Handler topic \'{self.topic_name}\' of subscriber \'{sub_name}\'", )
        raise Exception(message)

    def _log(self, message: str, sub_name:str):
        Logger().log(f"{message}",
                     log_name=f"Handler topic \'{self.topic_name}\' of subscriber \'{sub_name}\'", )




class SubscriberTopicFeatures(ABC, BaseModel):
    """
    - topic_name: str
    - queue_type: str
    - queue_size: int
    - drop_first: bool
    """
    model_config = ConfigDict(validate_default=True, frozen=True)

    topic_name: str
    queue_type: str
    queue_size: int
    drop_first: bool


class SubscriberConfig(BaseConfig):
    sub_name: str
    sub_topics_feats: conset(SubscriberTopicFeatures, min_length=1)
    handlers: conset(SubscriberHandler, min_length=1)


class Subscriber(ABC, BaseModel):
    """
    Sub define how to receive command (connector ~ framework) and how to react (update) for each topic. All inside topic.
    Subscriber is APP subscriber, not sub of framework such as ros.

    """

    sub_name: str = Field(...,frozen=True)
    sub_topics: conset(str, min_length=1)  = Field(...,frozen=True)
    queue_type: conset(str, min_length=1)  = Field(...,frozen=True)
    queue_size: conset(str, min_length=1)  = Field(...,frozen=True)

    _handlers_browser: dict[str,SubscriberHandler]
    _config: SubscriberConfig # for extra from child class.

    @validate_call
    def __init__(self, *,
                 sub_config: SubscriberConfig,
                 sub_handlers: set[SubscriberHandler]
                 ) :
        self._config = sub_config
        super().__init__(**self._extract_sub_config())
        self._add_handlers(sub_handlers)

        self._push_to_hub()
        self._notify_sub_info()


    def push_topic(self,topic: BaseTopic):
        pass

    def _extract_sub_config(self) -> dict:
        sub_config = dict(
            sub_name=self.config.sub_name,
            sub_topics={feat.topic_name for feat in self.config.sub_topics_feats},
            queue_type={feat.queue_type for feat in self.config.sub_topics_feats},
            queue_size={feat.queue_size for feat in self.config.sub_topics_feats},
        )
        return sub_config

    def _add_handlers(self, handlers: set[SubscriberHandler]):
        # Validate
        if len(handlers) != self.sub_topics:
            self._raise(
                f"Number of handlers must be equal to number of topics. But got {len(handlers)} and {len(self.sub_topics)}.")

        for handler in handlers:
            if handler.topic_name not in self.sub_topics:
                self._raise(f"Topic \'{handler.topic_name}\' of handler do not match with any subscriber's topics.")
        # Add
        for handler in handlers:
            self._handlers_browser[handler.topic_name] = handler

        self._log("Handlers were added successfully.")

    def _push_to_hub(self):
        """
        Assign topics to pub_sub_hub, topic should be predefined by inheriting BaseTopic.
        Storage and Hub will check if Publisher is valid to publish.
        """
        PubSubHub().add_subscriber(self)
        Logger().log(f"Register topics {self.sub_topics} successfully.", log_name=f"Subscriber \'{self.sub_name}\'")

    def _raise(self, message: str):
        Logger().log(f"Raise Exception: \"{message}\"", log_name=f"Subscriber \'{self.sub_name}\'", )
        raise Exception(message)

    def _log(self, message: str):
        Logger().log(f"{message}", log_name=f"Subscriber \'{self.sub_name}\'", )

    def _notify_sub_info(self): #TODO
        pass


    @validate_call
    def handle(self,
               topic: BaseTopic,
               **kwargs):

        if topic.topic_name not in self.sub_topics:
            self._raise(f"Subscriber {self.sub_name} haven't subscribed topic \"{topic.topic_name}\".")
            return None
        else:
            kwargs.update({'topic': topic})
            thread = Thread(target=self._call_handler,kwargs=kwargs)
            thread.start()
            return thread


    def _call_handler(self,topic: BaseTopic, **kwargs):
        self._handlers_browser[topic.topic_name].handle(topic=topic, subscriber=self, **kwargs)
