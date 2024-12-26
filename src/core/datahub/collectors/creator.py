from utils import Creator
from pydantic import Field
from typing import Union

from .images_collector import ImagesCollector

CollectorType = Union[ImagesCollector]

class CollectorCreator(Creator):
    object: CollectorType = Field(..., discriminator='cls_type')