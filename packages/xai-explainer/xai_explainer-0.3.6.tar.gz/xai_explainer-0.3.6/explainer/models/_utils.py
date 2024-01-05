from typing import List

from torch import Tensor, int64, sigmoid


def _sigmoid_output_handling(logits: Tensor) -> List[int]:
    assert (
        logits.ndim == 2
    ), "Expected logits to be 2-dimensional [batch_size, num_classes]"
    assert logits.shape[0] == 1, "Expected batch_size to be 1"

    probs = (sigmoid(logits) > 0.5).type(int64)
    class_indices = probs.nonzero(as_tuple=True)[1].tolist()

    return class_indices
