from pydantic import BaseModel, ConfigDict
from abc import abstractmethod,ABC
from pathlib import Path
import json

class BaseConfig(BaseModel,ABC):
    model_config = ConfigDict(validate_assignment=True,
                              validate_default= True,
                              extra='allow')
    primary_key:str

    @classmethod
    def load_json(cls, file: Path, primary_key: str):
        config_dict = json.loads(file.read_text())[primary_key]
        return cls(primary_key = primary_key,**config_dict)

    def dump_json(self, file: Path, primary_key: str):
        pass