from .datatype import DataType
import numpy as np
from typing import Literal
from typing_extensions import Self
from pydantic import model_validator, Field, ConfigDict


class Images(DataType):
    """
    cls_type: 'images'
    """
    cls_type: Literal['images']
    model_config = ConfigDict(arbitrary_types_allowed=True,
                              validate_assignment=True)

    images: np.ndarray
    height: int| None = None
    width: int| None = None

    @model_validator(mode = 'after')
    def validate_image_size(self) -> Self:
        if len(self.images.shape) != 4:
            raise ValueError('Images must have 4 dimensions.')

        if self.images.shape[1] != 3:
            raise ValueError(f"Images size must be (N,C,H,W), but got {self.images.shape}.")

        if self.height and self.images.shape[2] != self.height:
            raise ValueError(f"Images height must be {self.height}, but got {self.images.shape[2]}.")

        if self.width and self.images.shape[3] != self.width:
            raise ValueError(f"Images width must be {self.width}, but got {self.images.shape[3]}.")

        return self

