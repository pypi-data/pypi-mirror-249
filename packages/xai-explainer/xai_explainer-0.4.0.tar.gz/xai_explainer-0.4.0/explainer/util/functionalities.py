from functools import wraps
import logging
import time

import cv2 as cv
import numpy as np


def timeit(
    func=None,
    /,
    *,
    print_input: bool = False,
    print_output: bool = False,
    use_print: bool = False,
):
    def decorator_timeit(func):
        @wraps(func)
        def wrapper_timeit(*args, **kwargs):
            print_fn = print if use_print else logging.debug
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            if print_input:
                print_fn(f"@Timeit({func.__name__}) -> Input: {args}, {kwargs}")
            if print_output:
                print_fn(f"@Timeit({func.__name__}) -> Output: {result}")
            print_fn(
                f"@Timeit({func.__name__}) -> Execution time: {end_time - start_time} seconds"
            )
            return result

        return wrapper_timeit

    if func is None:  # @timeit() -> @timeit
        return decorator_timeit

    return decorator_timeit(func)


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def unify_string(string: str) -> str:
    """
    Unify a string by replacing whitespace with underscores and converting to lowercase.
    """

    return string.replace(" ", "_").lower()


# Credit: https://github.com/jacobgil/pytorch-grad-cam/blob/master/pytorch_grad_cam/utils/image.py#L33
def show_cam_on_image(
    img: np.ndarray,
    mask: np.ndarray,
    use_rgb: bool = False,
    colormap: int = cv.COLORMAP_JET,
    image_weight: float = 0.5,
) -> np.ndarray:
    """This function overlays the cam mask on the image as an heatmap.
    By default the heatmap is in BGR format.

    :param img: The base image in RGB or BGR format. Values are expected to be RGB or BGR in range [0, 255].
    :param mask: The cam mask. Values should be in the range [0, 1] and same height and width as the 'img'.
    :param use_rgb: Whether to use an RGB or BGR heatmap, this should be set to True if 'img' is in RGB format.
    :param colormap: The OpenCV colormap to be used.
    :param image_weight: The final result is image_weight * img + (1-image_weight) * mask.
    :returns: The default image with the cam overlay.
    """
    img = np.float32(img) / 255  # Scale to range [0, 1].
    heatmap = cv.applyColorMap(np.uint8(255 * mask), colormap)
    if use_rgb:
        heatmap = cv.cvtColor(heatmap, cv.COLOR_BGR2RGB)
    heatmap = np.float32(heatmap) / 255

    if np.max(img) > 1:
        raise Exception("The input image should np.float32 in the range [0, 1]")

    if image_weight < 0 or image_weight > 1:
        raise Exception(
            f"image_weight should be in the range [0, 1].\
                Got: {image_weight}"
        )

    cam = (1 - image_weight) * heatmap + image_weight * img
    cam = cam / np.max(cam)
    return np.uint8(255 * cam)
