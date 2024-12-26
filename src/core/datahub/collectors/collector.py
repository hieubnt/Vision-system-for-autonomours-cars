# Collectors are responsible to collect data from source.
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, ConfigDict

from utils import Creator

from ..sensors import Sensor



class DataCollector(ABC,BaseModel):
    """
    Base class for data collectors.
    """
    model_config =  ConfigDict(frozen=True)
    cls_type:str
    sensor: Sensor


