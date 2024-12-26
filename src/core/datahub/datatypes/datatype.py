from abc import ABC, abstractmethod
from pydantic import BaseModel
from utils import Creator

class DataType(BaseModel, ABC):
    cls_type: str




