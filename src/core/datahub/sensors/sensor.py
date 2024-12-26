# Module for making abstraction of all physical sensors,
# including processing physical signal and returning data.

from abc import ABC, abstractmethod
from typing import Any, Literal, Union
from pydantic import BaseModel, ConfigDict, Field, validate_call

from utils import Creator

from core.datahub.datatypes import DataType

class Sensor(ABC, BaseModel):
    """
    Base class for abstraction of physical sensors.
    """
    model_config = ConfigDict(frozen = True)
    
    cls_type: str
    queue_size: int

    @abstractmethod
    def _process_signal(self, raw_signal):
        pass

    @abstractmethod
    def get(self, **kwargs) -> Any:
        pass


class Camera(Sensor):
    cls_type: Literal['camera']

    def _process_signal(self, raw_signal):
        pass

    def get(self, **kwargs) -> Any:
        pass

class UltrasonicSensor(Sensor):
    cls_type: Literal['ultrasonic']

    def _process_signal(self, raw_signal):
        pass

    def get(self, **kwargs) -> Any:
        pass


SensorType = Union[Camera,UltrasonicSensor]
class SensorCreator(Creator):
    object: SensorType = Field(discriminator='cls_type')
    
        
        