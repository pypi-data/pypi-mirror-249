from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from PIL import Image
from lime import lime_image
import numpy as np
import torch
from torch import Tensor, nn

__all__ = [
    "VisionModel",
    "SegmentationModel",
    "ClassificationModel",
    "ExplainableModel",
    "XAI_Method",
    "XAI_Map",
    "XAI_Result",
    "XAI_MethodType",
    "register_method",
    "Cam",
    "LRP",
    "LIME",
]


VisionOutput = type("VisionOutput", (object,), {})

ClassificationOutput = type("ClassificationOutput", (VisionOutput,), {})

SegmentationOutput = type("SegmentationOutput", (VisionOutput,), {})


class XAI_MethodType(Enum):
    HEATMAP = 1
    EDGEMAP = 2
    SEGMENTS = 3


@dataclass
class XAI_Method:
    name: str = field(repr=True)
    method_type: XAI_MethodType = field(repr=True)
    method_handle: Callable[[Tensor, List[int]], np.ndarray] = field(repr=False)

    def __repr__(self):
        return f"XAI_Method(name={self.name}, method_type={self.method_type})"

    def __str__(self):
        return self.__repr__()


@dataclass(frozen=True)
class XAI_Map:
    """
    Dataclass for XAI maps and their metadata

    Attributes:
        map (np.ndarray): The XAI map
        method (XAI_Method): The method that was used to create the map
        target_class (int): The target class for which the map was created
    """

    map: np.ndarray = field(repr=False)
    method: XAI_Method = field(repr=True)
    predicted_label: int = field(repr=True)

    @property
    def method_name(self):
        return self.method.name

    @property
    def method_type(self):
        return self.method.method_type


@dataclass(frozen=True)
class XAI_Result:
    """
    Dataclass for explained inputs

    Attributes:
        original_image: The original image that was used to create the map
        input_tensor: The input tensor (device=cpu)
        predicted_labels: A list of predicted labels
        explanations_maps: A list of XAI maps
    """

    original_image: Image.Image = field(repr=False)
    input_tensor: Tensor = field(repr=False)
    predicted_labels: List[int] = field(repr=True)
    xai_maps: List[XAI_Map] = field(repr=True)

    def _resize_map(self, xai_map: np.ndarray, size: Tuple[int, int]) -> np.ndarray:
        h, w = size

        # Resize the XAI map to the original image size
        resized_map = Image.fromarray(xai_map).resize((w, h), resample=Image.BILINEAR)

        resized_map = np.array(resized_map)

        assert resized_map.shape[:2] == size

        return resized_map

    def get_resized_maps(
        self, size: Optional[Union[int, Tuple[int, int]]] = None
    ) -> List[XAI_Map]:
        """
        Resize all maps to the given size (width, height). If no size is given, the original image size is used.

        Args:
            size (Optional[Union[int, Tuple[int, int]]], optional): The size (h, w) to which the maps should be resized. If None, the original image size is used. Defaults to None.

        Returns:
            List[XAI_Map]: A list of resized XAI maps
        """

        if size is None:
            w, h = self.original_image.size
            size = (h, w)  # PIL uses (w, h), we use pytorch convention (h, w)
        elif isinstance(size, int):
            size = (size, size)

        return [
            XAI_Map(
                map=self._resize_map(xai_map.map, size),
                method=xai_map.method,
                predicted_label=xai_map.predicted_label,
            )
            for xai_map in self.xai_maps
        ]

    def group_py_label(self, resize_to_original_size=False) -> Dict[int, List[XAI_Map]]:
        """
        Group the XAI maps by their target class

        Args:
            resize_to_original_size (bool, optional): If True, the maps are resized to the original image size. Defaults to False.

        Returns:
            Dict[int, List[XAI_Map]]: A dictionary mapping from target class to a list of XAI maps
        """

        if resize_to_original_size:
            xai_maps = self.get_resized_maps()
        else:
            xai_maps = self.xai_maps

        grouped_maps = {}

        for xai_map in xai_maps:
            target_class = xai_map.predicted_label
            if target_class not in grouped_maps:
                grouped_maps[target_class] = []
            grouped_maps[target_class].append(xai_map)

        return grouped_maps


class TrainingModeManager:
    def __init__(self, model):
        self.model = model
        self.was_training = model.training

    def __enter__(self):
        self.model.eval()

    def __exit__(self, type, value, traceback):
        if self.was_training:
            self.model.train()


class FrozenModelManager:
    def __init__(self, model):
        self.model = model
        self.was_frozen = model.frozen

    def __enter__(self):
        self.model.unfreeze()

    def __exit__(self, type, value, traceback):
        if self.was_frozen:
            self.model.freeze()


class VisionModel(nn.Module):
    """
    Base class for vision models

    Args:
        num_classes (int): Number of output classes
        input_transform (Callable[[Image.Image], Tensor]): A callable that transforms the input image to a tensor
        output_handle (Callable[[Tensor], VisionOutput]): A callable that transforms the output tensor to a VisionOutput object
        meta_data (Dict[str, Any]): A dictionary containing any additional information that might be useful
    """

    def __init__(
        self,
        input_transform: Optional[Callable[[Image.Image], Tensor]] = None,
        output_handle: Optional[Callable[[Tensor], VisionOutput]] = None,
        meta_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()

        # Check that input transform and output handle are not implemented by subclass
        # This is to prevent the user from accidentally overwriting the default implementation
        if hasattr(self, "input_transform"):
            raise ValueError(
                "Attribute 'input_transform' is reserved for the default implementation"
            )

        if hasattr(self, "output_handle"):
            raise ValueError(
                "Attribute 'output_handle' is reserved for the default implementation"
            )

        self.input_transform = input_transform
        self.output_handle = output_handle
        self.meta_data = {} if meta_data is None else meta_data

        self._frozen = False

    @abstractmethod
    def forward(self, *args, **kwargs):
        """
        Forward pass logic

        :return: Model output
        """
        raise NotImplementedError

    def __str__(self):
        """
        Model prints with number of trainable parameters
        """
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + "\nTrainable parameters: {}".format(params)

    @property
    def device(self):
        return next(self.parameters()).device

    @property
    def num_params(self):
        return sum([np.prod(p.size()) for p in self.parameters()])

    @property
    def frozen(self):
        return self._frozen

    def _check_input_transform(self):
        if self.input_transform is None:
            raise NotImplementedError("Input transform must be implemented by subclass")

    def _check_output_handle(self):
        if self.output_handle is None:
            raise NotImplementedError("Output handle must be implemented by subclass")

    def _prepare_img(self, img: Union[Image.Image, Tensor]) -> Tensor:
        """Default implementation. This method can be overwritten by subclasses to provide additional functionality.

        Args:
            img (Union[Image.Image, Tensor]): The input image to run the model on. If an image is given, the input transform is applied beforehand. If a tensor is given, it is assumed that the input transform has already been applied.


        Raises:
            ValueError: If the input is neither an Image.Image nor a Tensor

        Returns:
            Tensor: The input tensor [1, c, h, w]
        """

        _is_tensor, _is_image = isinstance(img, Tensor), isinstance(img, Image.Image)

        if _is_tensor or _is_image:
            x = img if _is_tensor else self.input_transform(img)
            assert x.ndim in [
                3,
                4,
            ], f"Input must be 3-dimensional or 4-dimensional, but is {x.ndim}-dimensional"
            x = x.unsqueeze(0) if x.ndim == 3 else x
            x = x.to(self.device)
            return x

        raise ValueError(
            f"Input must be an Image.Image or a Tensor, but is {type(img)}"
        )

    def _predict(self, x: Tensor) -> VisionOutput:
        """Default implementation. This method can be overwritten by subclasses to provide additional functionality.

        Args:
            x (Tensor): The input tensor [1, c, h, w]. It is assumed that all transformations have already been applied so that the tensor can be directly fed into the model.
        Raises:
            NotImplementedError: If the input transform or output handle is not implemented by the subclass
            NotImplementedError: If the output handle is not implemented by the subclass

        Returns:
            VisionOutput: The output of the model (e.g. logits or probabilities for classification).
        """

        with torch.no_grad():
            out = self.forward(x)  # [1, num_output_neurons]
            out = self.output_handle(out)  # VisionOutput
        return out

    def predict(self, img: Union[Image.Image, Tensor]) -> VisionOutput:
        """Run the model on the given input image.

        Args:
            img  (Union[Image.Image, Tensor]): The input image to run the model on. If an image is given, the input transform is applied beforehand. If a tensor is given, it is assumed that the input transform has already been applied.

        Raises:
            NotImplementedError: If the input transform or output handle is not implemented by the subclass
            NotImplementedError: If the output handle is not implemented by the subclass

        Returns:
            VisionOutput: The output of the model (e.g. logits or probabilities for classification).
        """
        self._check_input_transform()
        self._check_output_handle()

        x = self._prepare_img(img)

        with TrainingModeManager(self):
            out = self._predict(x)

        return out

    def freeze(self):
        """
        Freeze all parameters
        """
        self._frozen = True
        for param in self.parameters():
            param.requires_grad = False

    def unfreeze(self):
        """
        Unfreeze all parameters
        """
        self._frozen = False
        for param in self.parameters():
            param.requires_grad = True


class SegmentationModel(VisionModel):
    """Segmentation model base class"""

    def predict(self, img: Image.Image) -> SegmentationOutput:
        return super().predict(img)


class ClassificationModel(VisionModel):
    """Classification model base class"""

    def __init__(self, num_classes, **kwargs) -> Any:
        super().__init__(**kwargs)
        assert num_classes is not None, "Number of classes must be specified"
        self.num_classes = num_classes

    def predict(self, img: Image.Image) -> ClassificationOutput:
        return super().predict(img)


AVAILABLE_METHODS = {}  # type: Dict[Tuple[str, str], XAI_Method]


def register_method(method_type, name=None, **method_kwargs):
    """Register a method for a class. Note: This decorator is applied at initialization time of the class.

    Args:
        method_type (MethodType): The type of the method
        name (str, optional): The name of the method. Defaults to None.
        **method_kwargs: Additional arguments that are passed to the method

    Raises:
        ValueError: If the method is already registered
    """

    def wrapper(fn: Callable[[Tensor, List[int]], XAI_Result]):
        nonlocal name

        name = name if name is not None else fn.__name__

        _cls = fn.__qualname__.split(".")[0]  # get the class name

        key = (_cls, name)

        method = XAI_Method(
            name=name,
            method_type=method_type,
            method_handle=partial(fn, **method_kwargs),
        )

        if key in AVAILABLE_METHODS:
            raise ValueError(f"An entry is already registered under the name '{key}'.")

        AVAILABLE_METHODS[key] = method

        return fn

    return wrapper


class ExplainableModel(ClassificationModel):
    """
    Base class for explainable models, i.e. models that can explain their predictions.
    """

    def _check_inputs_explain_classification(
        self, img, target_class, methods, tensor_image
    ):
        assert isinstance(
            img, Image.Image
        ), f"Input must be an Image.Image, but is {type(img)}"
        assert isinstance(
            target_class, int
        ), f"Target class must be an integer, but is {type(target_class)}"
        assert (
            isinstance(methods, list) and len(methods) > 0
        ), f"Methods must be a list of XAI_Methods, but is {type(methods)}"

        if tensor_image is not None:
            assert isinstance(
                tensor_image, Tensor
            ), f"Input tensor must be a Tensor, but is {type(tensor_image)}"
            assert (
                tensor_image.ndim == 4
            ), f"Input tensor must be 4-dimensional, but is {tensor_image.ndim}-dimensional"

    def _explain_classification(
        self,
        img: Image.Image,
        target_class: int,
        methods: List[str],
        tensor_image: Tensor,
    ) -> XAI_Result:
        """
        Default implementation. This method can be overwritten by subclasses to provide additional functionality.
        """
        xai_maps = [
            self.apply_xai_method(method, tensor_image, target_class)
            for method in methods
        ]

        return XAI_Result(
            original_image=img.copy(),
            input_tensor=tensor_image.detach().cpu(),
            predicted_labels=[target_class],
            xai_maps=xai_maps,
        )

    def explain_classification(
        self,
        img: Image.Image,
        target_class: int,
        methods: List[str],
        tensor_image: Tensor = None,
    ) -> XAI_Result:
        """
        Explain the classification-target on the given input image.

        Args:
            img (Image.Image): The input image to run the model on.
            target_class (int): The target class for which the explanation should be created.
            methods (List[str]): A list of method names that should be used to create the explanation.
            tensor_image (Tensor): The input tensor. If None, the tensor_image is created from the input image using the input transform. This is handy to speed up the explanation process if the same image is used for multiple explanations.

        Returns:
            An ExplainedInput object containing the explanation for the given target.
        """

        self._check_inputs_explain_classification(
            img, target_class, methods, tensor_image
        )
        if tensor_image is None:
            tensor_image = self._prepare_img(img)

        return self._explain_classification(img, target_class, methods, tensor_image)

    def explain(self, img: Image.Image, methods: List[str]) -> XAI_Result:
        assert isinstance(
            img, Image.Image
        ), f"Input must be an Image.Image, but is {type(img)}"

        classification_result: List[int] = self.predict(img)

        tensor_image = self._prepare_img(img)

        explanations = [
            self.explain_classification(img, idx, methods, tensor_image)
            for idx in classification_result
        ]

        merged_xai_maps = [
            xai_map for explanation in explanations for xai_map in explanation.xai_maps
        ]

        return XAI_Result(
            original_image=img,
            input_tensor=tensor_image.detach().cpu(),
            predicted_labels=sorted(classification_result),
            xai_maps=merged_xai_maps,
        )

    @classmethod
    def list_xai_methods(cls) -> List[str]:
        """
        List all available methods
        """
        # Get the names of all relevant classes in the method resolution order
        relevant_class_names = [
            _cls.__name__ for _cls in cls.mro() if issubclass(_cls, ExplainableModel)
        ]

        # Get the names of the methods for the relevant classes
        method_names = {
            method.name
            for key, method in AVAILABLE_METHODS.items()
            if key[0] in relevant_class_names
        }  # remove duplicates

        return sorted(method_names)

    @classmethod
    def get_xai_method(cls, method_name: str) -> XAI_Method:
        """
        Get the method object for the given method key

        Args:
            method_name: Name of the method

        Returns:
            The method object

        Raises:
            KeyError: If the method key is not available
        """

        # Get the names of all relevant classes in the method resolution order
        relevant_classes = [
            _cls for _cls in cls.mro() if issubclass(_cls, ExplainableModel)
        ]

        selected_class = None
        selected_method = None

        for _class in relevant_classes:
            class_name = _class.__name__
            if (class_name, method_name) in AVAILABLE_METHODS:
                if selected_class is None:
                    selected_class = _class
                    selected_method = AVAILABLE_METHODS[(class_name, method_name)]
                    continue

                # Warn if there are multiple methods withing the same inheritance level
                if _class not in selected_class.mro():
                    raise ValueError(
                        f"Multiple methods with name '{method_name}' found in class hierarchy of {cls.__name__} on the same inheritance level."
                    )

        if selected_method is not None:
            return selected_method
        else:
            raise KeyError(
                f"Method {method_name} not available for class {cls.__name__}"
            )

    def apply_xai_method(
        self, method_name: str, x: Tensor, target_class: int
    ) -> XAI_Map:
        """Apply a method to the given input image and target

        Args:
            method_name (str): Name of the method
            x (Tensor): Input tensor, transformations must be applied beforehand
            target_class (int): Target class

        Returns:
            XAI_Map: The result of the method
        """

        self._check_input_transform()

        method = self.get_xai_method(method_name)

        method_result = method.method_handle(self, x, target_class)
        assert isinstance(
            method_result, np.ndarray
        ), f"Expected numpy array but got {type(method_result)}"
        assert method_result.ndim in [2, 3]  # [h, w] or [h, w, c]

        xai_map = XAI_Map(
            map=method_result,
            method=method,
            predicted_label=target_class,
        )

        return xai_map


class InvalidInputError(Exception):
    pass


class Cam(ExplainableModel):
    """Basic CAM implementation"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def _cam_target_layers(self):
        """
        Needs to be implemented by the subclass
        """
        raise NotImplementedError()

    def _cam_reshape_transform(self):
        """
        Can be overwritten by the subclass
        """

        return None

    @property
    def cam_target_layers(self) -> Optional[Callable]:
        """
        Needs to be implemented by the subclass
        """
        return self._cam_target_layers()

    @property
    def cam_reshape_transform(self):
        return self._cam_reshape_transform()

    def _validate_cam_inputs(self, x, idx):
        if not isinstance(x, Tensor):
            raise InvalidInputError("Input must be a tensor")
        if not isinstance(idx, int):
            raise InvalidInputError("Target class must be an integer")
        if len(x.shape) != 4:
            raise InvalidInputError(
                f"Input must be a 4-dimensional tensor, but has shape {x.shape}"
            )
        if x.shape[0] != 1:
            raise InvalidInputError(
                f"Input must have a batch size of 1, but has batch size {x.shape[0]}"
            )
        if x.shape[1] != 3:
            raise InvalidInputError(
                f"Input must have 3 channels, but has {x.shape[1]} channels"
            )

    @register_method(
        XAI_MethodType.HEATMAP,
        name="gradcam",
        method="gradcam",
        aug_smooth=True,
        eigen_smooth=True,
    )
    @register_method(
        XAI_MethodType.HEATMAP,
        name="gradcam++",
        method="gradcam++",
        aug_smooth=True,
        eigen_smooth=True,
    )
    @register_method(
        XAI_MethodType.HEATMAP,
        name="xgradcam",
        method="xgradcam",
        aug_smooth=True,
        eigen_smooth=True,
    )
    @register_method(
        XAI_MethodType.HEATMAP,
        name="eigengradcam",
        method="eigengradcam",
        aug_smooth=True,
        eigen_smooth=True,
    )
    def _cam(
        self,
        x: Tensor,
        class_index: int,
        **kwargs,
    ) -> np.ndarray:
        self._validate_cam_inputs(x, class_index)

        return self._cam_impl(
            model=self,
            input_tensor=x,
            category_index=class_index,
            target_layers=self.cam_target_layers,
            **kwargs,
        )

    @staticmethod
    def _cam_impl(
        model,
        input_tensor,
        category_index,
        target_layers,
        method="gradcam",
        aug_smooth=False,
        eigen_smooth=False,
    ):
        from pytorch_grad_cam import EigenGradCAM, GradCAM, GradCAMPlusPlus, XGradCAM
        from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

        methods = {
            "gradcam": GradCAM,
            "gradcam++": GradCAMPlusPlus,
            "xgradcam": XGradCAM,
            "eigengradcam": EigenGradCAM,
        }

        cam = methods[method](
            model=model,
            target_layers=target_layers,
            reshape_transform=model.cam_reshape_transform,
        )

        # use_cuda is deprecated -> it is now inferred from the model
        # if an error occurs, update grad-cam to version 1.5 (pip install grad-cam==1.5)

        targets = [ClassifierOutputTarget(category_index)]
        heatmap = cam(
            input_tensor=input_tensor,
            targets=targets,
            eigen_smooth=aug_smooth,
            aug_smooth=eigen_smooth,
        )  # ndarray of shape [1, h, w]

        heatmap = heatmap.squeeze(0)  # [h, w]

        return heatmap


class LRP(ExplainableModel):
    """Basic LRP implementation"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_epsilongamma",
        method="epsilon_gamma",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_epsilonplus",
        method="epsilon_plus",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_epsilonplusflat",
        method="epsilon_plusflat",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_epsilonalpha2beta1",
        method="epsilon_alpha2beta1",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_epsilonalpha2beta1flat",
        method="epsilon_alpha2beta1flat",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_guidedbackprop",
        method="guided_backprop",
    )
    @register_method(
        XAI_MethodType.EDGEMAP,
        name="lrp_excitationbackprop",
        method="excitation_backprop",
    )
    def _lrp(
        self,
        x: Tensor,
        class_index: int,
        **kwargs,
    ) -> np.ndarray:
        return self._lrp_impl(
            model=self,
            input_tensor=x,
            category_index=class_index,
            **kwargs,
        )

    @staticmethod
    def _lrp_impl(
        model,
        input_tensor,
        category_index,
        method="epsilon_gamma",
    ):
        from zennit.attribution import Gradient
        from zennit.canonizers import SequentialMergeBatchNorm
        from zennit.composites import (
            EpsilonAlpha2Beta1,
            EpsilonAlpha2Beta1Flat,
            EpsilonGammaBox,
            EpsilonPlus,
            EpsilonPlusFlat,
            ExcitationBackprop,
            GuidedBackprop,
        )

        canonizers = [SequentialMergeBatchNorm()]

        methods = {
            "epsilon_gamma": EpsilonGammaBox(low=-3.0, high=3.0, canonizers=canonizers),
            "epsilon_plus": EpsilonPlus(canonizers=canonizers),
            "epsilon_plusflat": EpsilonPlusFlat(canonizers=canonizers),
            "epsilon_alpha2beta1": EpsilonAlpha2Beta1(canonizers=canonizers),
            "epsilon_alpha2beta1flat": EpsilonAlpha2Beta1Flat(canonizers=canonizers),
            "guided_backprop": GuidedBackprop(canonizers=canonizers),
            "excitation_backprop": ExcitationBackprop(canonizers=canonizers),
        }
        use_cuda = model.device.type == "cuda"
        with Gradient(model=model, composite=methods[method]) as attributor:
            _, rel = attributor(
                input_tensor,
                torch.eye(model.num_classes)[[category_index]].to(
                    "cuda" if use_cuda else "cpu"
                ),
            )

        rel = rel.squeeze(0)
        rel = torch.mean(rel, dim=0)  # TODO

        return rel.detach().cpu().numpy()


class LIME(ExplainableModel):
    """Basic LIME implementation"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Disabled for now!
    # @register_method(
    #    XAI_MethodType.SEGMENTS,
    #    name="lime_segments",
    #    method="lime_segments",
    # )
    @register_method(
        XAI_MethodType.HEATMAP,
        name="lime",
        method="lime_heatmap",
    )
    def _lime(
        self,
        x: Tensor,
        class_index: int,
        **kwargs,
    ) -> np.ndarray:
        return self._lime_impl(
            model=self,
            input_tensor=x,
            category_index=class_index,
            **kwargs,
        )

    @staticmethod
    def _lime_impl(
        model,
        input_tensor,
        category_index,
        method="lime_heatmap",
    ):
        model.eval()
        use_cuda = model.device.type == "cuda"

        # define predict funtion to get class probabilities
        def _predict_lime(x):
            """Predict the class probabilities for the given input tensor

            Parameters
            ----------
            x : NDarray
                Input numpy array

            Returns
            -------
            List[float]
                Class probabilities
            """
            x = torch.from_numpy(x).permute(0, 3, 1, 2)
            if use_cuda:
                x = x.to("cuda")

            with torch.no_grad():
                out = model.forward(x)
            probs = torch.softmax(out, dim=1)
            return probs.detach().cpu().numpy()

        # visualize relevant super-pixels and their importance
        def explanation_heatmap(exp, exp_class):
            """
            Using heat-map to highlight the importance of each super-pixel for the model prediction
            https://towardsdatascience.com/how-to-explain-image-classifiers-using-lime-e364097335b4
            """
            dict_heatmap = dict(exp.local_exp[exp_class])
            heatmap = np.vectorize(dict_heatmap.get)(exp.segments)
            # plt.imshow(heatmap, cmap="RdBu", vmin=-heatmap.max(), vmax=heatmap.max())
            # plt.colorbar()
            # plt.show()
            return heatmap

        def wrapped_slic(image, n_segments=100, compactness=10.0):
            from skimage.segmentation import slic

            # Convert image to uint8 if necessary
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)

            # Apply skimage's slic function
            segments = slic(image, n_segments=n_segments, compactness=compactness)

            print(segments.shape)
            return segments

        def wraped_segment_anything_huge(image):
            from explainer.parts_extraction import get_segmentation_method

            # Convert image to uint8 if necessary
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)

            segmentation = get_segmentation_method("segment_anything_huge")
            segments = segmentation.forward(img=image, maps=None)

            return segments

        # create explainer
        explainer = lime_image.LimeImageExplainer(verbose=False)
        # convert input to numpy
        input = input_tensor[0].detach().cpu().numpy().transpose(1, 2, 0)
        # explain input
        explanation = explainer.explain_instance(
            input,
            _predict_lime,
            top_labels=5,
            num_samples=1000,
            batch_size=1,
            # segmentation_fn=wraped_segment_anything_huge,
        )

        # from matplotlib import pyplot as plt
        # from skimage.segmentation import mark_boundaries
        # get mask with the top 5 relevant segments
        temp, mask = explanation.get_image_and_mask(category_index, num_features=5)
        # mark segemnts on input
        # img_boundry = mark_boundaries(temp, mask)
        # Display the image with the mask applied
        # plt.imshow(img_boundry)
        # plt.title("Most relevant superpixels")
        # plt.show()

        heatmap = explanation_heatmap(explanation, explanation.top_labels[0])

        if method == "lime_segments":
            raise NotImplementedError()
            return mask
        elif method == "lime_heatmap":
            return heatmap
        else:
            raise ValueError(f'Unknown method "{method}"')
