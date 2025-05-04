import numpy as np
from numba import jit

dde_val = 1


def dde_change(value):
    global dde_val
    dde_val = value


def median3x3(image):
    processing_image = np.zeros_like(image)
    for i in range(1, 512 - 2):
        for j in range(1, 640 - 2):
            processing_image[i][j] = med3(image[i - 1: i + 2, j - 1: j + 2])
    return processing_image.astype(np.uint16)


@jit(nopython=True)
def median5x5(image):
    processing_image = np.zeros_like(image)
    for i in range(2, 512 - 3):
        for j in range(2, 640 - 3):
            part = image[i - 2: i + 3, j - 2: j + 3]
            #     part = np.sort(part.flatten())
            part = part.flatten()
            processing_image[i][j] = part[12] / 2 + part[11] / 8 + part[13] / 8 + part[17] / 8 + part[7] / 8
    return processing_image.astype(np.uint16)


@jit(nopython=True)
def med3(part):
    part = part.flatten()
    part = np.sort(part)
    m_med = part[4]
    return m_med


@jit(nopython=True)
def dde(image, k):
    image = image.astype(np.float64)
    processing_image = np.zeros_like(image)
    for i in range(1, 512 - 2):
        for j in range(1, 640 - 2):
            pxl = image[i][j]
            elem = pxl * k
            if elem < -32576:
                elem = -32576
            if elem > 32576:
                elem = 32576
            processing_image[i][j] = elem
    return processing_image.astype(np.int32)


@jit(nopython=True)
def get_hf(image, low_image):
    image = image.astype(np.int32)
    low_image = low_image.astype(np.int32)
    high_image = np.zeros_like(image)
    for i in range(512):
        for j in range(640):
            if (j == 0) or (j == 639) or (i == 0) or (i == 511):
                high_image[i][j] = image[i][j] - low_image[i][j]
            else:
                high_image[i][j] = image[i][j] - low_image[i][j]
    return high_image


@jit(nopython=True)
def min_max(image):
    processing_image = np.zeros_like(image)
    for i in range(1, 512 - 1):
        for j in range(1, 640 - 1):
            m00 = image[i - 1][j - 1]
            m01 = image[i - 1][j]
            m02 = image[i - 1][j + 1]

            m10 = image[i][j - 1]
            m11 = image[i][j]
            m12 = image[i][j + 1]

            m20 = image[i + 1][j - 1]
            m21 = image[i + 1][j]
            m22 = image[i + 1][j + 1]

            min_0 = min(min(m00, m01), m02)
            min_1 = min(min(m10, m11), m12)
            min_2 = min(min(m20, m21), m22)
            m_min = min(min(min_0, min_1), min_2)

            max_0 = max(max(m00, m01), m02)
            max_1 = max(max(m10, m11), m12)
            max_2 = max(max(m20, m21), m22)
            m_max = max(max(max_0, max_1), max_2)

            processing_image[i][j] = m_min / 2 + m_max / 2

    return processing_image.astype(np.uint16)


@jit(nopython=True)
def sumFreqs(high, lowMid):
    processing_image = np.zeros_like(lowMid).astype(np.int32)
    for i in range(0, 512):
        for j in range(0, 640):
            elem = (high[i][j] + lowMid[i][j])
            if elem < 0:
                elem = 0
            elif elem > 65535:
                elem = 65535
            processing_image[i][j] = elem
    return processing_image.astype(np.uint16)


def generate_map(local_size):
    map = np.zeros((512, 640))
    dim_x = 512 // local_size
    dim_y = 640 // local_size
    cnt_x = 0
    for m in range(0, 512, local_size):
        cnt_y = 0
        for l in range(0, 640, local_size):
            for i in range(0, local_size):
                for j in range(0, local_size):
                    x = i + m
                    y = j + l

                    ind_x1 = (m + i + local_size // 2) // local_size - 1
                    if ind_x1 < 0:
                        x1 = - local_size // 2
                        x2 = local_size // 2
                    elif ind_x1 == dim_x - 1:
                        x2 = 512 + local_size // 2
                        x1 = 512 - local_size // 2
                    else:
                        x1 = local_size // 2 + ind_x1 * local_size
                        x2 = x1 + local_size

                    ind_y1 = (l + j + local_size // 2) // local_size - 1
                    if ind_y1 < 0:
                        y1 = - local_size // 2
                        y2 = local_size // 2
                    elif ind_y1 == dim_y - 1:
                        y2 = 640 + local_size // 2
                        y1 = 640 - local_size // 2
                    else:
                        y1 = local_size // 2 + ind_y1 * local_size
                        y2 = y1 + local_size

                    dx1 = np.abs(x - x1)
                    dx2 = np.abs(x - x2)
                    dy1 = np.abs(y - y1)
                    dy2 = np.abs(y - y2)

                    min_x = min(dx1, dx2)
                    min_y = min(dy1, dy2)

                    k1 = (x2 - x) * (y2 - y)
                    k2 = (x - x1) * (y2 - y)
                    k3 = (x2 - x) * (y - y1)
                    k4 = (x - x1) * (y - y1)

                    if min_x == dx1 and min_y == dy1:
                        map[x][y] = k1
                    if min_x == dx1 and min_y == dy2:
                        map[x][y] = k3
                    if min_x == dx2 and min_y == dy1:
                        map[x][y] = k2
                    if min_x == dx2 and min_y == dy2:
                        map[x][y] = k4
            cnt_y += 1
        cnt_x += 1

    return map
