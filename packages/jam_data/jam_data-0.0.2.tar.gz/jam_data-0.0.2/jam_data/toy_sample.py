from io import BytesIO
from typing import Optional, Union

import requests
import torch
from PIL import Image
from torchvision import transforms

__all__ = ["get_image_example", "url_to_tensor"]


def url_to_tensor(url: str, size: Optional[Union[int, tuple]] = None) -> torch.Tensor:
    # Download the image
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Resize if size is specified
    if size is not None:
        if isinstance(size, tuple) or isinstance(size, list):
            assert len(size) == 2, "Size must be a tuple or list of length 2"
            image = image.resize([size[1], size[0]])
        elif isinstance(size, int):
            image = image.resize((size, size))

    # Convert to tensor
    transform = transforms.ToTensor()
    tensor_image = transform(image)
    return tensor_image


DUMMY_TOY_SAMPLE = {
    "4k": "https://gitlab.com/qsh.zh/dummy_data/-/raw/456643ea13fd62ffa1341b27eac249496eba7b7e/images/church4k.jpg",
    "church": "https://gitlab.com/qsh.zh/dummy_data/-/raw/456643ea13fd62ffa1341b27eac249496eba7b7e/images/church4k.jpg",
}


def get_image_example(key: str, *args, **kwargs) -> torch.Tensor:
    if key in DUMMY_TOY_SAMPLE:
        url = DUMMY_TOY_SAMPLE[key]
    elif key.startswith("http"):
        url = key
    else:
        raise ValueError(f"Invalid key {key}")
    return url_to_tensor(url, *args, **kwargs)


if __name__ == "__main__":
    tensor_image = get_image_example("4k", size=[1024, 2048])
    print(tensor_image.shape)  # Print tensor shape to verify
