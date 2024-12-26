# from __future__ import annotations
from pydantic import validate_call, BaseModel, ConfigDict, conset, model_validator
from typing_extensions import Self


class TopicInfo(BaseModel):
    """
    Fields:\n
    - pub_name: str\n
    - sub_names: set[str]

    Model validator: 'pub_name' and 'sub_names' cannot be None together.
    """
    model_config = ConfigDict(validate_assignment=True)
    pub_name: str | None
    sub_names: conset(str, min_length=1) | None

    @model_validator(mode='after')
    def check_valid_init(self) -> Self:
        if self.pub_name is None and self.sub_names is None:
            raise ValueError("\'pub_name\' and \'sub_names\' cannot be None together.")
        return self

    @validate_call
    def merge_info(self, other: BaseModel) -> None:
        if not isinstance(other, TopicInfo):
            raise Exception('\'merge_info\' only accept value of type \'TopicInfo\'.')
        if other.pub_name is not None:
            if self.pub_name is not None:
                raise ValueError(
                    f"\'pub_name\': \'{self.pub_name}\' has already existed but received another: \'{other.pub_name}\'")
            self.pub_name = other.pub_name

        for sub in self.sub_names:
            for sub2 in other.sub_names:
                if sub == sub2:
                    raise ValueError(f"\'sub_name\': \'{sub}\' is repeated in two TopicInfo objects.'")
        self.sub_names = self.sub.union(other.sub_names)


TopicInfo.model_rebuild()


class TopicSet(BaseModel):
    """
    Fields:\n
    - topic_names: set[str]
    """
    model_config = ConfigDict(validate_assignment=True)
    topic_names: conset(str, min_length=1)


class HubStorage:
    """
    Class for storing and managing, control collisions of Publishers, Subscribers and Topics.\n
    All Topics must be added when add Publishers or Subscribers. So that no options to add topics if Pubs or Subs are already added.\n
    - Each Publisher will have unique set of Topics.\n
    - Each Topic will be owned by only one Publisher. But can have multiple Subscribers.\n
    - There always need at least one Publisher or Subscriber hold the topic.\n


    API:\n
    - add_publisher(...) : add one publisher and its topics.\n
    - add_subscriber(...): add one subscriber and its topics.\n
    - check_publisher(...): check if publisher have already been added. Return an info dict or empty dict.\n
    - check_subscriber(...): check if subscriber have already been added. Return an info dict or empty dict.\n
    - check_topic(...): check if topic exist. Return an info else return None.\n


    """

    def __init__(self):
        self._pubs_info: dict[str, TopicSet] = dict()
        self._subs_info: dict[str, TopicSet] = dict()
        self._topics_info: dict[str, TopicInfo] = dict()

    @validate_call
    def add_publisher(self, pub_name: str, topic_names: str | set[str]) -> None:
        """
        Will raise error if:

        - 'pub_name' has already existed.

        - 'topic_names' has already existed.

        - param's types do not match with type hint.
        :param pub_name:
        :param topic_names:
        :return:
        """
        if isinstance(topic_names, str):
            topic_names = {topic_names}
        self._check_new_publisher(pub_name, topic_names)

        self._pubs_info[pub_name] = TopicSet(topic_names=topic_names)
        self._update_topics_info(topic_names, pub_name=pub_name)

    @validate_call
    def add_subscriber(self, sub_name: str, topic_names: str | set[str]) -> None:
        """
        Will raise error if:

        :param sub_name:
        :param topic_names:
        :return:
        """
        if isinstance(topic_names, str):
            topic_names = {topic_names}
        self._check_new_subscriber(sub_name)

        self._subs_info[sub_name] = TopicSet(topic_names=topic_names)
        self._update_topics_info(topic_names, sub_names={sub_name})

    @validate_call
    def check_publisher(self, pub_name: str) -> TopicSet | None:
        """
        :param pub_name:
        :return: if publisher exists, return a dict(pub_name = TopicSet), else return empty dict.
        """
        if pub_name in self._pubs_info.keys():
            return self._pubs_info[pub_name]
        else:
            return None

    @validate_call
    def check_subscriber(self, sub_name: str) -> TopicSet | None:
        """
        :param sub_name:
        :return: if subscriber exists, return a dict(sub_name = TopicSet), else return empty dict.
        """
        if sub_name in self._subs_info.keys():
            return self._subs_info[sub_name]
        else:
            return None

    @validate_call
    def check_topic(self, topic_name: str) -> TopicInfo | None:
        """
        :param topic_name:
        :return: if topic exists, return a dict(topic_name = TopicInfo), else return empty dict.
        """
        if topic_name in self._topics_info.keys():
            return self._topics_info[topic_name]
        else:
            return None

    def _check_new_publisher(self, pub_name: str, topic_names: set[str]) -> None:
        """
        Check if publisher and topics have not existed yet. Raise if they existed.
        :param pub_name:
        :param topic_names:
        :return:
        """
        if self.check_publisher(pub_name):
            raise Exception(f'Publisher \'{pub_name}\' already exists.')

        for topic_name in topic_names:
            check = self.check_topic(topic_name)
            if check:
                raise Exception(f'Topic \'{topic_names} was registered by {check[topic_name].pub_name}.\'')

    def _check_new_subscriber(self, sub_name: str) -> None:
        """
        check if subscriber have not existed yet. Raise if it existed.
        :param sub_name:
        :return:
        """
        if self.check_subscriber(sub_name):
            raise Exception(f'Subscriber \'{sub_name}\' already exists.')

    def _update_topics_info(self,
                            topic_names: set[str],
                            *,
                            pub_name: str = None,
                            sub_names: set[str] = None):

        # See definition of TopicInfo to know how to check error.
        topic_info = TopicInfo(pub_name=pub_name, sub_names=sub_names)

        for topic_name in topic_names:
            if topic_name not in self._topics_info.keys():
                self._topics_info[topic_name] = topic_info
            else:
                self._topics_info[topic_name].merge_info(topic_info)
