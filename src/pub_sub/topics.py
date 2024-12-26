from abc import ABC
from pydoc_data.topics import topics

from pydantic import BaseModel, Field, validate_call, ConfigDict
import numpy as np
from typing import Literal, Union


#  Each topic has unique datatype, data abstract,... So I wrap topic name with data type validation.
# Topic is created mean that data format is enough

# USING BY APP


class BaseTopic(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)
    topic_name: str


class StatusTopic(BaseTopic):
    topic_name: Literal['status']
    status: Literal['ACTIVE', 'PENDING', 'NONACTIVE']


class ImagesTopic(BaseTopic):
    topic_name: Literal['images']
    images: list[np.ndarray]

    class Config:
        arbitrary_types_allowed = True


class InputImagesTopic(ImagesTopic):
    """
    Input images from source such as camera, image stream, ...
    """
    topic_name: Literal['input_images']


class DrawnImagesTopic(ImagesTopic):
    topic_name: Literal['drawn_images']


class SegmentedImagesTopic(BaseTopic):
    topic_name: Literal['segmented_images']
    images: list[np.ndarray]

    class Config:
        arbitrary_types_allowed = True


Topic_Type = Union[StatusTopic, ImagesTopic, DrawnImagesTopic, SegmentedImagesTopic]


class TopicCreator(BaseModel):
    """
    Factory for all topics.
    """
    topic: Topic_Type = Field(..., discriminator='topic_name')

    @classmethod
    @validate_call
    def create(cls,*, data: dict, topic_name: str|None = None) -> BaseTopic:
        if topic_name:
            topic_input = {'topic_name': topic_name}
            topic_input.update(data)
            return cls(topic = topic_input).topic
        else:
            return cls(topic = data).topic


