from fnmatch import fnmatch
import logging
from typing import Dict, Iterable, List, Tuple, Union

from matplotlib import pyplot as plt
import torch
import torch.nn as nn
from torchvision import models

from explainer.models.base import ExplainableModel, XAI_Result
from explainer.util import filehandling

from .modules import PeakResponseMapping


def finetune(
    model: nn.Module,
    base_lr: float,
    groups: Dict[str, float],
    ignore_the_rest: bool = False,
    raw_query: bool = False,
) -> List[Dict[str, Union[float, Iterable]]]:
    """Fintune."""

    print("finetune------->> ", base_lr, groups, ignore_the_rest, raw_query)

    parameters = [
        dict(
            params=[],
            names=[],
            query=query if raw_query else "*" + query + "*",
            lr=lr * base_lr,
        )
        for query, lr in groups.items()
    ]
    rest_parameters = dict(params=[], names=[], lr=base_lr)
    for k, v in model.named_parameters():
        for group in parameters:
            if fnmatch(k, group["query"]):
                group["params"].append(v)
                group["names"].append(k)
            else:
                rest_parameters["params"].append(v)
                rest_parameters["names"].append(k)
    if not ignore_the_rest:
        parameters.append(rest_parameters)
    for group in parameters:
        group["params"] = iter(group["params"])
    return parameters


class FC_ResNet(nn.Module):
    def __init__(self, pretrained, num_classes, **kwargs):
        super(FC_ResNet, self).__init__()
        model = models.resnet50(pretrained)

        # feature encoding
        self.features = nn.Sequential(
            model.conv1,
            model.bn1,
            model.relu,
            model.maxpool,
            model.layer1,
            model.layer2,
            model.layer3,
            model.layer4,
        )

        # classifier
        num_features = model.layer4[1].conv1.in_channels
        self.classifier = nn.Sequential(
            nn.Conv2d(num_features, num_classes, kernel_size=1, bias=True)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class PRM(PeakResponseMapping, ExplainableModel):
    def __init__(self, num_classes, pretrained=True):
        ExplainableModel.__init__(self)
        PeakResponseMapping.__init__(
            self,
            enable_peak_stimulation=True,
            enable_peak_backprop=True,
            win_size=3,
            sub_pixel_locating_factor=8,
            filter_type="median",
        )

        self.backbone = FC_ResNet(pretrained, num_classes)
        self.add_module("backbone", self.backbone)

    def forward(self, input, class_threshold=0.2, peak_threshold=1, retrieval_cfg=None):
        x = super(PRM, self).forward(
            input,
            class_threshold=class_threshold,
            peak_threshold=peak_threshold,
            retrieval_cfg=retrieval_cfg,
        )
        return x

    def _apply(self, x) -> Tuple[List[List[int]], torch.Tensor]:
        """Perform multi-label binary classification on x

        Args:
        -------
            x : torch.Tensor, shape=(N, C, H, W) N=batch_size, C=channels, H=height, W=width

        Returns
        -------
        Tuple[List[List[int]], torch.Tensor]
            Tuple of class indices and output tensor
        """

        self.eval()
        if x is None:
            return
        output = self(x)
        if output is None:
            return

        pred = torch.sigmoid(output)
        pred = (pred > 0.5).type(torch.int64)

        class_indices = []
        for p in pred:
            # get all indices where p == 1 for the current sample
            tmp = p.nonzero().flatten().tolist()
            class_indices.append(tmp)

        return class_indices, output

    def explain(self, x):
        """Classify x and return heatmaps for each class/category

        Arguments
        ---------
        x : torch.Tensor shape=(N, C, H, W) N=batch_size, C=channels, H=height, W=width

        Returns
        -------
        List[ExplainedInput]
            Heatmap and Label for each input in batch
        """

        pred_list = []
        self.eval()

        for i in range(x.shape[0]):
            input = x[i]

            # unsqueeze to (1, C, H, W)
            if input.ndim == 3:
                input = input.unsqueeze(0)
            pred_list, pred = self._apply(input)

            # get class indices for first sample
            pred_list = pred_list[0]
            num_classes = len(pred_list)

            logging.debug(f"Raw predictions: {pred}")

            # Enable gradient computation for peak response maps
            with torch.enable_grad():
                input.requires_grad = True
                self.inference()
                visual_cues = self(input)

            if visual_cues is None:
                logging.warning("No visual cues found!!!")
                pred_list = []
                continue

            (
                confidences,  # (1, num_classes)
                class_response_maps,  # (1, num_classes, H, W)
                class_peak_responses,  # (num_peak_response_maps, [0, class_idx, peak_x, peak_y])
                peak_response_maps,  # (num_peak_response_maps, H, W)
            ) = visual_cues
            num_peak_response_maps = len(peak_response_maps)

            # get class scores (1,) of first sample
            class_scores = confidences[0][pred_list].tolist()

            # debugging
            logging.debug(f"class_scores: {class_scores}")
            logging.debug(f"pred_list: {pred_list}")
            logging.debug(
                f"Got {num_classes} predicted classes and {num_peak_response_maps} peak response maps"
            )

            # enable/disable plots for testing
            plot = True
            if plot:
                # prepare subplots
                num_plots = 2 + len(peak_response_maps)
                f, axarr = plt.subplots(
                    1 + num_classes,
                    num_plots,
                    figsize=(num_plots * 3, (1 + num_classes) * 3),
                )

                # plot input image
                axarr[0, 0].imshow(input.detach()[0].permute(1, 2, 0).cpu())
                axarr[0, 0].set_title(f"Image (transformed) classes={pred_list}")
                axarr[0, 0].axis("off")

                # remove unused subplots
                for i in range(1, num_plots):
                    f.delaxes(axarr[0, i])

                # plot class response maps
                for idx, class_idx in enumerate(pred_list):
                    axarr[idx + 1, 0].imshow(
                        class_response_maps[0, class_idx].cpu(), interpolation="none"
                    )
                    axarr[idx + 1, 0].set_title(
                        f"CRM class_idx={class_idx} score={round(class_scores[idx], ndigits=2)}"
                    )
                    axarr[idx + 1, 0].axis("off")

            # initialize merged peak response map
            merged_peak_response_map = torch.zeros(num_classes, 224, 224).cpu()

            # indices for current y-axis for each class
            counters = [2] * num_classes

            for prm, peak in sorted(
                zip(peak_response_maps, class_peak_responses),
                key=lambda v: v[-1][-1],
            ):
                curr_class_idx = peak[1].item()
                if plot:
                    # plot peak response map
                    axs_x = counters[pred_list.index(curr_class_idx)]
                    counters[pred_list.index(curr_class_idx)] += 1
                    axs_y = pred_list.index(curr_class_idx) + 1
                    axarr[axs_y, axs_x].imshow(prm.cpu(), cmap=plt.cm.jet)
                    axarr[axs_y, axs_x].set_title(
                        f"PRM peak=({peak[2].item()},{peak[3].item()})"
                    )
                    axarr[axs_y, axs_x].axis("off")

                # mormalize peak response map
                prm /= torch.max(prm)

                # merge peak response maps of current class
                merged_peak_response_map[pred_list.index(curr_class_idx)] += prm.cpu()

            if plot:
                # plot merged peak response map
                for idx, merged_prm in enumerate(merged_peak_response_map):
                    axarr[idx + 1, 1].imshow(merged_prm, cmap=plt.cm.jet)
                    axarr[idx + 1, 1].set_title("Merged PRMs")
                    axarr[idx + 1, 1].axis("off")

                # remove empty subplots
                for ax_y in range(num_classes):
                    for ax_x in range(counters[ax_y], num_plots):
                        f.delaxes(axarr[ax_y + 1, ax_x])

                cwd = filehandling.get_working_dir()
                plt.savefig(cwd / "tmp" / "crms_and_prms.png")

        # return an ExplainableInput for each sample
        explanations = [
            XAI_Result(
                input_tensor=x[i],
                predicted_labels=pred_list,
                explanations=[prm for prm in merged_peak_response_map],
                # explanations=[
                #    crm / torch.max(crm)
                #    for idx, crm in enumerate(class_response_maps[0])
                #    if idx in pred_list
                # ],
                use_logits=True,
            )
            for i in range(x.shape[0])
        ]
        return explanations
