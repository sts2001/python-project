import base64

import cv2
import numpy as np


def image_array_to_base64(img_array: np.ndarray, format_: str = ".jpg") -> str:
    success, buffer = cv2.imencode(format_, img_array)
    if not success:
        raise ValueError("Ошибка при кодировании изображения")

    base64_str = base64.b64encode(buffer).decode("utf-8")
    return base64_str


def base64_to_ndarray(base64_str: str):
    base64_ext = None
    if "," in base64_str:
        a = base64_str.split(",")
        base64_str = a[1]
        base64_ext = "." + a[0].split("/")[1]

    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img, base64_ext
