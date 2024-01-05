__all__ = ["list_datasets", "get_dataset"]

from typing import List, Type

from explainer.datasets.base import VisionDataset

REGISTERED_DATASET = {}


def register_dataset(cls) -> Type[VisionDataset]:
    REGISTERED_DATASET[cls.__name__] = cls
    return cls


def list_datasets() -> List[str]:
    """Return a list of registered dataset names.

    Returns:
        List[str]: List of registered dataset names.
    """
    return list(REGISTERED_DATASET.keys())


def get_dataset(name: str) -> Type[VisionDataset]:
    """Return a dataset class by name.

    Args:
        name (str): Name of the dataset.

    Returns:
        Type[VisionDataset]: Dataset class.

    Raises:
        KeyError: If the dataset is not registered.
    """
    return REGISTERED_DATASET[name]
