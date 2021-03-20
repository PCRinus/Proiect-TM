import sys
import cv2
import numpy as np

if len(sys.argv) != 3:
    raise(NameError("Usage: <script.py> <cale_spre_imagine> <tip_sablon>"))

tip_sablon = sys.argv[1]

src = cv2.imread(f"poze/{sys.argv[1]}")

sablon = cv2.imread(f"sabloane/{sys.argv[2]}.png")

if sablon is None:
    sablon = cv2.imread(f"sabloane/{sys.argv[2]}.jpg")
    if sablon is None:
        raise(NameError("Nu exista acel sablon"))

src = cv2.resize(src, sablon.shape[1::-1])
src = cv2.cvtColor(src, cv2.COLOR_RGB2RGBA)

print(src.shape)

lower_black = np.array([0, 0, 0], dtype="uint8")
upper_black = np.array([130, 130, 130], dtype="uint8")
black_mask = cv2.inRange(sablon, lower_black, upper_black)

for i in range(0, src.shape[0]):
    for j in range(0, src.shape[1]):
        if black_mask[i][j] == 0:
            src[i][j][3] = 0


border = np.zeros(src.shape, dtype="uint8")

border_size = 1

for i in range(border_size, src.shape[0] - border_size):
    for j in range(border_size, src.shape[1] - border_size):
        if src[i][j][3] == 0 and (src[i][j+border_size][3] != 0 or src[i][j-border_size][3] != 0 or src[i+border_size][j][3] != 0 or src[i-border_size][j][3] != 0):
            border[i][j] = [0, 0, 0, 255]

for i in range(0, src.shape[0]):
    for j in range(0, src.shape[1]):
        if border[i][j][3] != 0 and src[i][j][3] == 0:
            src[i][j] = border[i][j]

cv2.imwrite('result.png', src)
