from functools import lru_cache
from typing import List

from PIL import Image
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from torchvision import transforms

from explainer.datasets.base import ClassificationDataset

from ..util.geo_estimator import Partitioning, download_cell_partitionings
from ._api import register_dataset

__all__ = ["Im2GPS"]


@register_dataset
class Im2GPS(ClassificationDataset):
    @staticmethod
    def transform(img: Image):
        size = (224, 224)
        return transforms.Compose(
            [
                transforms.Resize(size),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ]
        )(img)

    @staticmethod
    def classes() -> List[str]:
        classes = list(
            map(
                list,
                zip(*[partitioning().get_lat_lng(c) for c in range(12893)]),
            )
        )
        return list(map(list, zip(*classes)))

    def get_place_from_coords(lat, lng):
        geolocator = Nominatim(user_agent="xai")
        try:
            location = geolocator.reverse([lat, lng], exactly_one=True, language="en")
            address = location.raw["address"]
            city = address.get("city", "Unknown")
            country = address.get("country", "Unknown")
        except GeocoderUnavailable:
            city = "NO CONNECTION"
            country = "NO CONNECTION"

        return city, country


@lru_cache(maxsize=1)
def partitioning():
    partitionings_dict = download_cell_partitionings()
    NUM_HEADER_ROWS = 2

    for shortname, file in zip(
        partitionings_dict["shortnames"],
        partitionings_dict["files"],
    ):
        if shortname == "fine":
            return Partitioning(file, shortname, skiprows=NUM_HEADER_ROWS)

    raise ValueError("fine partitioning not found")
