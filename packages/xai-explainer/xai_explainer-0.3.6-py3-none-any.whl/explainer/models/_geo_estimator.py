from typing import List

import torch
import torchvision

from explainer.datasets import Im2GPS

from ..util.geo_estimator import Hierarchy, Partitioning, download_cell_partitionings
from ._api import ModelType, register_model
from .base import LIME, LRP, Cam

__all__ = [
    "MultiPartitioningClassifier",
]


@register_model(
    model_type=ModelType.OBJECT_MODEL,
    weights_url="https://tu-dortmund.sciebo.de/s/eZVHXx2QRzCPJU9/download",
    dataset=Im2GPS,
    name="geo_estimator",
    config={
        "num_classes": Im2GPS.num_classes(),
        "input_transform": Im2GPS.transform,
    },
)
class MultiPartitioningClassifier(Cam, LRP, LIME):
    def __init__(self, **kwargs):
        super().__init__(
            output_handle=lambda x: [torch.argmax(x, dim=1).item()], **kwargs
        )

        partitionings = download_cell_partitionings()
        self.partitionings, self.hierarchy = self.__init_partitionings(partitionings)
        self.model, self.classifier = self.__build_model()

    def __init_partitionings(self, partitionings_dict):
        partitionings = []
        for shortname, file in zip(
            partitionings_dict["shortnames"],
            partitionings_dict["files"],
        ):
            NUM_HEADER_ROWS = 2
            partitionings.append(
                Partitioning(file, shortname, skiprows=NUM_HEADER_ROWS)
            )

        if len(partitionings_dict["files"]) == 1:
            return partitionings, None

        return partitionings, Hierarchy(partitionings)

    def __build_model(self):
        model, nfeatures = build_base_model()

        classifier = torch.nn.ModuleList(
            [
                torch.nn.Linear(nfeatures, len(self.partitionings[i]))
                for i in range(len(self.partitionings))
            ]
        )
        return model, classifier

    def forward(self, x):
        fv = self.model(x)
        yhats = [self.classifier[i](fv) for i in range(len(self.partitionings))]
        return self._geo_guessr_output_handling(yhats)

    def _cam_target_layers(self):
        for name, layer in self.model.named_modules():
            if name == "7.2":
                return [layer]

    def _geo_guessr_output_handling(self, out: List[torch.Tensor]) -> List[int]:
        yhats = [torch.nn.functional.softmax(yhat, dim=1) for yhat in out]
        yhats = [torch.reshape(yhat, (1, 1, *list(yhat.shape[1:]))) for yhat in yhats]

        yhats = [torch.max(yhat, dim=1)[0] for yhat in yhats]

        hierarchy_preds = None
        if self.hierarchy is not None:
            hierarchy_logits = torch.stack(
                [yhat[:, self.hierarchy.M[:, i]] for i, yhat in enumerate(yhats)],
                dim=-1,
            )
            hierarchy_preds = torch.prod(hierarchy_logits, dim=-1)

            # hierarchy_preds = [torch.argmax(hierarchy_preds, dim=1).item()]
        return hierarchy_preds


def build_base_model():
    # from torchvision.models.resnet import ResNet50_Weights
    # model = torchvision.models.__dict__[arch](weights=ResNet50_Weights.DEFAULT)

    model = torchvision.models.__dict__["resnet50"]()

    nfeatures = model.fc.in_features
    model = torch.nn.Sequential(*list(model.children())[:-2])

    model.avgpool = torch.nn.AdaptiveAvgPool2d(1)
    model.flatten = torch.nn.Flatten(start_dim=1)
    return model, nfeatures
