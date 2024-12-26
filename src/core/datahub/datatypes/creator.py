from utils import Creator
from typing import Union
from pydantic import Field

from .images import Images

DataType = Union[Images]

class DataCreator(Creator):
    object: DataType = Field(...,discriminator='cls_type')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)