import sys
import cv2
import numpy as np


def remove_opacity(src, mask):
    """
    Compares source image to mask and changes the source pixels opacity:
    - mask pixel is white -> src has opacity
    - mask pixel is black -> src doesn't have opacity
    """
    for i in range(0, src.shape[0]):
        for j in range(0, src.shape[1]):
            if mask[i][j] == 0:
                src[i][j][3] = 0


def compute_border(src, border_size=1):
    """

    """
    border = np.zeros(src.shape, dtype="uint8")

    for i in range(border_size, src.shape[0] - border_size):
        for j in range(border_size, src.shape[1] - border_size):
            if src[i][j][3] == 0 and (src[i][j+border_size][3] != 0 or src[i][j-border_size][3] != 0 or src[i+border_size][j][3] != 0 or src[i-border_size][j][3] != 0):
                border[i][j] = [0, 0, 0, 255]

    return border


def add_border(src, border):
    """

    """
    for i in range(0, src.shape[0]):
        for j in range(0, src.shape[1]):
            if border[i][j][3] != 0 and src[i][j][3] == 0:
                src[i][j] = border[i][j]


if __name__ == '__main__':

    if len(sys.argv) != 3:
        raise (NameError("Usage: <script.py> <cale_spre_imagine> <tip_sablon>"))

    src = cv2.imread(f"poze/{sys.argv[1]}")
    sablon = cv2.imread(f"sabloane/{sys.argv[2]}.png", 0)

    if sablon is None:
        sablon = cv2.imread(f"sabloane/{sys.argv[2]}.jpg", 0)
        if sablon is None:
            raise (NameError("Nu exista acel sablon"))

    src = cv2.resize(src, sablon.shape[::-1])  # resize takes resolution inverted

    src = cv2.cvtColor(src, cv2.COLOR_RGB2RGBA)

    remove_opacity(src, sablon)

    opacity_border = compute_border(src, border_size=1)

    add_border(src, opacity_border)

    cv2.imwrite('result.png', src)
