from pydantic import BaseModel, Field, validate_call
from typing import Any
import json
from pathlib import Path
from abc import ABC, abstractmethod

class Creator(BaseModel,ABC):
    """
    Base class for all factories using Pydantic style

    - Creators must have field name object: Union[...] = Field(..., discriminator = cls_type)
    - All product class must have field cls_type: Literal[...]

    """
    object: Any

    @classmethod
    @validate_call
    def create(cls, cls_type:str, **kwargs) -> Any:
        cfg = {'cls_type': cls_type}
        cfg.update(kwargs)

        return cls(object = cfg).object


    @classmethod
    @validate_call
    def create_from_json(cls, json_cfg: Path|str, primary_key:str):

        if isinstance(json_cfg, Path):
            json_cfg = json_cfg.read_text()

        cfg = json.loads(json_cfg)[primary_key]

        return cls(object = cfg).object