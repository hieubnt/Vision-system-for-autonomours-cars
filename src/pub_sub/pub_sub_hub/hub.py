from utils.singleton import SingletonMeta
from utils.list_tools import pack_list_if_not
from logger.logger import Logger
from pydantic import validate_call, conset, BaseModel
from threading import Thread

from .storage import HubStorage
from ..topics import BaseTopic
from ..subscriber import Subscriber
from ..publisher import Publisher
from .message_queues import BaseMessageQueue


#Hub or sub hold connector ??
# class SubConnectorBrow(BaseModel):
#     topics: conset(str,min_length=1)
#     connectors: conset(BaseConnector,min_length=

# where to queue, pub, sub or both ?
# Each sub has to define how to handle queue.
# Worker for each sub or for all sub ? if subs, cannot know entire system how many worker. So hub  hold worker, also queue #TODO
#Sub define queuetype.
# __queues_browser: dict[str, BaseMessageQueue] and searcher
# sub define, hub hold and process
#HUB hold entire n_ threads

class HubWorker(Thread, BaseModel):

    topic: BaseTopic
    subscribers: conset(Subscriber,min_length= 1)


    def __init__(self,*,topic: BaseTopic, subscribers: set[Subscriber], **kwargs):

        super(BaseModel,self).__init__(topic = topic, subscribers = subscribers)
        super(Thread,self).__init__(**kwargs)

        self.start()


    def _push_topic(self):
        Logger(f"Worker start pushing topic {self.topic.name}.")
        for sub in self.subscribers:
            sub.push_topic(self.topic)
            Logger(f"Worker pushed topic {self.topic.name} to {sub.sub_name}.")
        Logger(f"Worker pushed topic {self.topic.name} to all subscribers.")


    def run(self):
        self._push_topic()





# Worker search or manager s earhc ??  search inverse
# Workers move forward but the searcher is the last. if there is topic, worker do it.

# Subscriber define type of queues message, because it know what to drop.

# TODO


class PubSubHub (metaclass=SingletonMeta):
    """ Singleton class that handle all framework. Base on Facade pattern.

        One topic should be used by only one publisher.

        Publisher can have multiple handlers for multiple topics.


    """
    # @validate_call

    def __init__(self,
                 *,
                 max_workers: int|None = None):
        # n_worker is none mean infinity workers
        self.max_workers = max_workers
        self.storage = HubStorage()
        self.sub_browser: dict[str,set[Subscriber]] = dict()
        """keys is topic_name (str)"""
        # topic_name: queue

    @validate_call
    def add_publisher(self, publisher:Publisher) -> None:
        HubStorage().add_publisher(publisher.pub_name, publisher.pub_topics)


    @validate_call()
    def add_subscriber(self, subscriber: Subscriber):
        HubStorage().add_subscriber(subscriber.sub_name, subscriber.sub_topics)
        self.sub_browser[subscriber.sub_name] = subscriber


    @validate_call
    def publish(self, topic: BaseTopic) -> HubWorker:
        worker = HubWorker(topic=topic, subscribers = self.sub_browser[topic.topic_name], daemon = True )
        return worker



























