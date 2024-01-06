from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Callable, List, Optional, Type, TypeVar, Union
import warnings

from torch.hub import load_state_dict_from_url

from explainer.datasets.base import VisionDataset

from .base import VisionModel

__all__ = [
    "get_model_dir",
    "set_model_dir",
    "ModelType",
    "register_model",
    "list_models",
    "get_model",
    "fetch_model_class",
    "fetch_model_class",
    "fetch_model_xai_methods",
    "fetch_model_dataset",
]


REGISTERED_MODELS = {}
MODEL_DIR = None
WARNING_DISPLAYED = False


def set_model_dir(model_dir: str) -> None:
    global MODEL_DIR
    MODEL_DIR = model_dir


def get_model_dir() -> str:
    global WARNING_DISPLAYED
    global MODEL_DIR
    if MODEL_DIR is None and not WARNING_DISPLAYED:
        # warn user that it will default to torch.hub.get_dir()
        warnings.warn(
            "Model directory is not set. Defaulting to torch.hub.get_dir().",
            UserWarning,
        )
        WARNING_DISPLAYED = True

    return MODEL_DIR


class ModelType(Enum):
    OBJECT_MODEL = "object_model"
    PARTS_MODEL = "parts_model"
    SEGMENTATION_MODEL = "segmentation_model"

    @staticmethod
    def from_str(model_type: str) -> "ModelType":
        model_type = model_type.lower()
        if model_type == "object_model":
            return ModelType.OBJECT_MODEL
        elif model_type == "parts_model":
            return ModelType.PARTS_MODEL
        elif model_type == "segmentation_model":
            return ModelType.SEGMENTATION_MODEL
        else:
            raise ValueError(f"Unknown model type {model_type}")


@dataclass(frozen=True)
class RegisteredModel:
    model_builder: Callable[..., VisionModel]
    model_type: ModelType
    config: Optional[dict]
    weights_url: Optional[str]
    dataset: Optional[Type[VisionDataset]]

    @staticmethod
    def _check_dataset_type(dataset, dataset_type):
        return dataset is not None and (
            isinstance(dataset, dataset_type)
            or (isinstance(dataset, type) and issubclass(dataset, dataset_type))
        )

    @cached_property
    def model_class(self) -> type:
        return self.get_model().__class__

    @cached_property
    def _file_name(self) -> str:
        """Returns the file name of the weights file."""
        from hashlib import md5

        return md5(self.weights_url.encode("utf-8")).hexdigest()

    def get_model(self) -> VisionModel:  # TODO long running time
        """Returns an initialized model with the given configuration.

        Args:
            **kwargs: The configuration for the model.

        Returns:
            BaseModel: The initialized model.
        """
        model = self.model_builder(**self.config)  # <-- this may take a long time

        if self.weights_url is not None:
            state_dict = load_state_dict_from_url(
                url=self.weights_url,
                model_dir=get_model_dir(),
                file_name=self._file_name,
                map_location="cpu",
            )

            model.load_state_dict(state_dict)

        return model


M = TypeVar("M", bound=VisionModel)


def register_model(
    model_type: ModelType,
    config: Optional[dict] = None,
    weights_url: Optional[str] = None,
    dataset: Optional[Type[VisionDataset]] = None,
    name: Optional[str] = None,
) -> Callable[[Callable[..., M]], Callable[..., M]]:
    """Registers a model with the given configuration under the given name.

    Args:
        model_type (ModelType): The type of the model.
        weights_url (str): The url to the weights file.
        config (dict): The configuration for the model.
        dataset (Optional[ClassificationDataset] ): The dataset the model was trained on. Defaults to None.
        name (Optional[str], optional): The name under which the model is registered. Defaults to None.

    Returns:
        Callable[[Callable[..., M]], Callable[..., M]]: The decorator.
    """

    def wrapper(fn: Callable[..., M]) -> Callable[..., M]:
        key = name if name is not None else fn.__name__

        registered_model = RegisteredModel(
            model_builder=fn,
            model_type=model_type,
            config=config,
            weights_url=weights_url,
            dataset=dataset,
        )

        if key in REGISTERED_MODELS:
            raise ValueError(f"An entry is already registered under the name '{key}'.")

        REGISTERED_MODELS[key] = registered_model

        return fn

    return wrapper


def list_models(model_type: Optional[Union[ModelType, str]] = None) -> List[str]:
    all_models = sorted(list(REGISTERED_MODELS.keys()))

    if model_type is None:
        return all_models

    if isinstance(model_type, str):
        model_type = ModelType.from_str(model_type)

    return [
        model
        for model in all_models
        if REGISTERED_MODELS[model].model_type == model_type
    ]


def _get_registered_model(name: str) -> RegisteredModel:
    try:
        registered_model = REGISTERED_MODELS[name]
    except KeyError:
        raise ValueError(f"Unknown model {name}")
    return registered_model


def get_model(name: str) -> VisionModel:
    """
    Gets the model name and configuration and returns an instantiated model.

    Args:
        name (str): The name under which the model is registered.

    Returns:
        model (BaseModel): The initialized model.
    """
    return _get_registered_model(name).get_model()


def fetch_model_class(name: str) -> type:
    """
    Gets the model name and returns the model class.

    Args:
        name (str): The name under which the model is registered.

    Returns:
        model (BaseModel): The model class.
    """
    return _get_registered_model(name).model_class


def fetch_model_xai_methods(name: str) -> List[str]:
    """
    Get the available xai methods for the given model.

    Args:
        name (str): The name under which the model is registered.

    Returns:
        List[str]: Names of the available xai methods that can be applied to the model.
    """

    return fetch_model_class(name).list_xai_methods()


def fetch_model_dataset(name: str) -> Optional[Type[VisionDataset]]:
    """
    Get the dataset the model was trained on.

    Args:
        name (str): The name under which the model is registered.

    Returns:
        Optional[Type[ClassificationDataset]]: The dataset the model was trained on.
    """
    return _get_registered_model(name).dataset
