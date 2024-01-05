import numpy as np
from timm.models.vision_transformer import VisionTransformer
import torch
from torch import Tensor, nn
from transformers import ViTForImageClassification, ViTImageProcessor

from explainer.datasets.imagenet import ImageNet
from explainer.datasets.pascal import Pascal

from ._api import ModelType, register_model
from ._utils import _sigmoid_output_handling
from .base import LRP, Cam, ClassificationModel, XAI_MethodType, register_method

__all__ = ["ViT_XAI"]


class ViT_XAI(Cam, LRP):
    _IMG_SIZE = 224

    def __init__(
        self,
        vit: VisionTransformer,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.vit = vit

        self.vit.head = nn.Linear(
            self.vit.head.in_features, self.num_classes
        )  # Replace the last layer

        # Disable fused attention for gradient rollout
        # https://github.com/jacobgil/vit-explain/issues/23
        for block in self.vit.blocks:
            block.attn.fused_attn = False

        self._grad_rollout_handle = VITAttentionGradRollout(
            model=self, discard_ratio=0.9
        )

    def forward(self, x):
        return self.vit(x)

    def _cam_target_layers(self):
        return [self.vit.blocks[-1].norm1]

    def _cam_reshape_transform(self):
        def reshape_transform(tensor, height=14, width=14):
            result = tensor[:, 1:, :].reshape(
                tensor.size(0), height, width, tensor.size(2)
            )

            # Bring the channels to the first dimension,
            # like in CNNs.
            result = result.transpose(2, 3).transpose(1, 2)
            return result

        return reshape_transform

    @register_method(XAI_MethodType.HEATMAP, name="gradient_rollout")
    def _grad_rollout(self, x: Tensor, class_index: int, **kwargs) -> np.ndarray:
        x = self._grad_rollout_handle(
            input_tensor=x, category_index=class_index
        )  # [H, W] e.g. [14, 14]

        return x.detach().cpu().numpy()


class VITAttentionGradRollout:
    def __init__(self, model, attention_layer_name="attn_drop", discard_ratio=0.9):
        self.model = model
        self.discard_ratio = discard_ratio

        for name, module in self.model.named_modules():
            if attention_layer_name in name:
                module.register_forward_hook(self.get_attention)
                module.register_full_backward_hook(self.get_attention_gradient)

        self.attentions = []
        self.attention_gradients = []

    def _reset(self):
        self.attentions = []
        self.attention_gradients = []

    def get_attention(self, module, input, output):
        self.attentions.append(output.cpu())

    def get_attention_gradient(self, module, grad_input, grad_output):
        self.attention_gradients.append(grad_input[0].cpu())

    def __call__(self, input_tensor, category_index):
        self._reset()
        self.model.zero_grad()
        output = self.model(input_tensor)
        device = next(self.model.parameters()).device.type
        category_mask = torch.zeros(output.size(), device=device)
        category_mask[:, category_index] = 1
        loss = (output * category_mask).sum()
        loss.backward()

        return self.grad_rollout(
            self.attentions, self.attention_gradients, self.discard_ratio
        )

    @staticmethod
    def grad_rollout(attentions, gradients, discard_ratio):
        result = torch.eye(attentions[0].size(-1))
        with torch.no_grad():
            for attention, grad in zip(attentions, gradients):
                weights = grad
                attention_heads_fused = (attention * weights).mean(axis=1)
                attention_heads_fused[attention_heads_fused < 0] = 0

                # Drop the lowest attentions, but
                # don't drop the class token
                flat = attention_heads_fused.view(attention_heads_fused.size(0), -1)
                _, indices = flat.topk(int(flat.size(-1) * discard_ratio), -1, False)
                # indices = indices[indices != 0]
                flat[0, indices] = 0

                I = torch.eye(attention_heads_fused.size(-1))  # noqa E741
                a = (attention_heads_fused + 1.0 * I) / 2
                a = a / a.sum(dim=-1)
                result = torch.matmul(a, result)

        # Look at the total attention between the class token,
        # and the image patches
        mask = result[0, 0, 1:]
        # In case of 224x224 image, this brings us from 196 to 14
        width = int(mask.size(-1) ** 0.5)
        mask = mask.reshape(width, width)
        mask = mask / mask.max()
        return mask


@register_model(
    model_type=ModelType.OBJECT_MODEL,
    weights_url="https://tu-dortmund.sciebo.de/s/jFdXY3k0uVIb1XS/download",
    dataset=Pascal,
    name="vit_xai_pascal",
    config={
        "num_classes": Pascal.num_classes(),
        "input_transform": Pascal.transform,
        "output_handle": _sigmoid_output_handling,
    },
)
def vit_base(**kwargs):
    basemodel = torch.hub.load(
        "facebookresearch/deit:main", "deit_base_patch16_224", pretrained=False
    )

    return ViT_XAI(basemodel, **kwargs)


@register_model(
    model_type=ModelType.PARTS_MODEL,
    dataset=ImageNet,
    name="vit_parts_b_16_224",
    config={
        "num_classes": ImageNet.num_classes(),
        "pretrained": "google/vit-base-patch16-224",
    },
)
@register_model(
    model_type=ModelType.PARTS_MODEL,
    dataset=ImageNet,
    name="vit_parts_l_16_224",
    config={
        "num_classes": ImageNet.num_classes(),
        "pretrained": "google/vit-large-patch16-224",
    },
)
class ViT_Parts(ClassificationModel):
    def __init__(self, pretrained: str, **kwargs):
        processor = ViTImageProcessor.from_pretrained(pretrained)

        _input_transform = lambda x: processor(  # noqa E731
            images=x, return_tensors="pt"
        )
        _output_handle = lambda x: [x.argmax(-1).item()]  # noqa E731

        super().__init__(
            input_transform=_input_transform, output_handle=_output_handle, **kwargs
        )
        # ("google/vit-base-patch16-224"
        self.vit = ViTForImageClassification.from_pretrained(pretrained)

    def forward(self, x):
        outputs = self.vit(**x)
        logits = outputs.logits
        return logits

    def _prepare_img(self, x):
        return self.input_transform(x).to(self.device)
