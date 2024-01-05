import numpy as np
import cv2
from PIL import Image

from fastcv import cast, info, view

if __name__ == "__main__":
    x_pil = Image.open("assets/fastcv.webp")
    print(info(x_pil))
    view(x_pil)

    x_cv2 = cast(x_pil, type="cv2", color="bgr")
    print(info(x_cv2))
    view(x_cv2)

    # cv2.imshow("main", x_cv2)
    # cv2.waitKey(0)
    # print(x_cv2.get().dtype)

    # cast from tensor to numpy
    # x = np.random.randn(1, 3, 224, 224).astype(np.float32)

    # x = cast(x, type="tensor", dtype="fp32")
    exit()
