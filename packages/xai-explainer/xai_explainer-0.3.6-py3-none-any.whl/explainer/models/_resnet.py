from torch import nn
from torchvision import models

from explainer.datasets.pascal import Pascal, PascalParts

from ._api import ModelType, register_model
from ._utils import _sigmoid_output_handling
from .base import LRP, Cam, ClassificationModel

__all__ = [
    "ResNet",
    "ResNet_XAI",
]


class ResNet(ClassificationModel):
    def __init__(self, resnet, **kwargs):
        super().__init__(**kwargs)
        self.pretrained = resnet

        self.pretrained.fc = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, self.num_classes),
        )

    def forward(self, x):
        return self.pretrained(x)


class ResNet_XAI(ResNet, Cam, LRP):
    def _cam_target_layers(self):
        return [self.pretrained.layer4[-1]]


@register_model(
    model_type=ModelType.OBJECT_MODEL,
    weights_url="https://tu-dortmund.sciebo.de/s/2UeO47mYjEx5YKt/download",
    dataset=Pascal,
    config={
        "num_classes": Pascal.num_classes(),
        "input_transform": Pascal.transform,
        "output_handle": _sigmoid_output_handling,
    },
)
def resnet50_xai_voc(**kwargs):
    resnet = models.resnet50(weights=None)
    return ResNet_XAI(resnet, **kwargs)


@register_model(
    model_type=ModelType.PARTS_MODEL,
    weights_url="https://tu-dortmund.sciebo.de/s/7fAxd4RMPcg1drr/download",
    dataset=PascalParts,
    config={
        "num_classes": PascalParts.num_classes(),
        "input_transform": PascalParts.transform,
        "output_handle": _sigmoid_output_handling,
    },
)
def resnet50_parts_voc(**kwargs):
    resnet = models.resnet50(weights=None)
    return ResNet(resnet, **kwargs)
