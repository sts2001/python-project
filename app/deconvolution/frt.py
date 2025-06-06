import cv2 as cv
import numpy as np

import app.deconvolution.image_processing as imp

from app.utils.frt import (base64_to_ndarray,
                           image_array_to_base64)


class Deconvolution:
    @staticmethod
    def get(img):
        frt_data, extension = base64_to_ndarray(img)
        frt_data = frt_data[np.newaxis, :, :]
        for i in frt_data:
            frt_orig = i
            frt = np.mean(frt_data, axis=0)[231:281, 275:325]
            frt = frt[17 - 1:20 + 1, 24 - 1:27 + 1]
            frt = frt - 24 * 1024
            frt = frt / np.sum(frt)
            a11 = frt[1, 1]
            a12 = frt[1, 2]
            a13 = frt[1, 3]
            a21 = frt[2, 1]
            a22 = frt[2, 2]
            a23 = frt[2, 3]
            a31 = frt[3, 1]
            a32 = frt[3, 2]
            a33 = frt[3, 3]
            c11 = frt[0, 0]
            c12 = frt[0, 1]
            c13 = frt[0, 2]
            c14 = frt[0, 3]
            c15 = frt[0, 4]
            c21 = frt[1, 0]
            c25 = frt[1, 4]
            c31 = frt[2, 0]
            c35 = frt[2, 4]
            c41 = frt[3, 0]
            c45 = frt[3, 4]
            c51 = frt[4, 0]
            c52 = frt[4, 1]
            c53 = frt[4, 2]
            c54 = frt[4, 3]
            c55 = frt[4, 4]

            B = [[1, 0, 0, 0, 0, 0, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, a12, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, a13, a12, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, a13, a12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 0, 0, a13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, a21, 0, 0, 0, 0, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1 + a22, a21, 0, 0, 0, a12, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, a23, 1 + a22, a21, 0, 0, a13, a12, a11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, a23, 1 + a22, 0, 0, 0, a13, a12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, a23, 1, 0, 0, 0, a13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, a31, 0, 0, 0, 1, a21, 0, 0, 0, 0, a11, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, a32, a31, 0, 0, 0, 1 + a22, a21, 0, 0, 0, a12, a11, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, a33, a32, a31, 0, 0, a23, 1 + a22, a21, 0, 0, a13, a12, a11, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, a33, a32, 0, 0, 0, a23, 1 + a22, 0, 0, 0, a13, a12, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, a33, 0, 0, 0, 0, a23, 1, 0, 0, 0, a13, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a31, 0, 0, 0, 1, a21, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a32, a31, 0, 0, 0, 1 + a22, a21, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, a32, a31, 0, 0, a23, 1 + a22, a21, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, a32, 0, 0, 0, a23, 1 + a22, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, 0, 0, 0, 0, a23, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a31, 0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a32, a31, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, a32, a31, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, a32, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a33, 0, 0, 0, 0, 0, 1]]
            C = np.array(
                [c11, c12, c13, c14, c15, c21, 0, 0, 0, c25, c31, 0, 0, 0, c35, c41, 0, 0, 0, c45, c51, c52, c53, c54,
                 c55])
            B = np.array(B)
            B[:, 12] = B[:, 12] + C
            U = np.zeros(25)
            U[12] = 1.0
            mask = np.dot(np.linalg.inv(B), U).reshape((5, 5))
            mask = mask / np.sum(mask)

            tank_frt = cv.filter2D(frt_orig, -1, mask)

            return f"data:image/{extension[1:]};base64,{image_array_to_base64(tank_frt, extension)}"
