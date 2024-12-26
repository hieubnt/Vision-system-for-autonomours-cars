from core.datahub.datatypes import DataCreator
from core.datahub.datatypes.images import Images
import numpy as np
import pytest

def test_images():
    images = np.ones((4, 3, 225, 225))
    images2 = np.ones((4, 5, 225, 225))
    try:
        test1 = DataCreator.create(cls_type = "images", images = images)

        assert isinstance(test1, Images), type(test1)
        assert test1.images.shape == (4, 3, 225, 225)
        print(test1.images.shape[3])


    except Exception as e:
        pytest.fail(f"Fail with exception: {e}.")

    with pytest.raises(Exception) as e:
        test2 = DataCreator.create(cls_type = "images", images = images2)
        test3 = DataCreator.create(cls_type = "images", images = images, height = 100,width = 100)

