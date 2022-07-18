import cv2
import numpy as np
import matplotlib.pyplot as plt

# create the cropped image based on downloaded image
img = cv2.imread(r"C:\Users\lowel\Downloads\connect 4.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
cropped_board = hsv_img[110:550, 0:520]
# cropped_board = hsv_img[80:320, 80:400]
shape = cropped_board.shape

# find values that are necessary to access specific pixels
rows = 6
columns = 7

height = shape[0] // rows
width = shape[1] // columns

y1 = (height // 2)
x1 = (width // 2)

# define an array that is the correct size with values that are all zeros
arr = np.zeros([6, 7], dtype=int)


# Take the average hue of a certain range of pixels
def average_color(i, j):
    y = y1 + (height * i)
    x = x1 + (width * j)
    n = 1
    old_value = 0

    for p in range(10):
        for o in range(10):
            colors = cropped_board[y - 5 + o, x - 5 + p]
            new = colors[0]
            average = (new + old_value) / n
            n += 1
            old_value += new
            cropped_board[y - 5 + o, x - 5 + p] = [0, 0, 100]
    return average


# upload values to the array
# **opencv Interprets colors in BGR and Matplotlib is in RGB**
for i in range(rows):
    for j in range(columns):
        h = average_color(i, j)

        if (85 < h) & (h < 105):
            arr[i][j] = 1

        elif (110 < h) & (h < 130):

            arr[i][j] = -1

        else:
            arr[i][j] = 0
        print(h)

print(arr)


def diag1_check(i, j, color):
    evaluation = 1
    # checks values to the right and down of the point
    m = 1
    for x in range(3):
        if ((i + m) > 5) or ((j + m) > 6):
            break
        elif arr[i + m][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and up of the point
    n = 1
    for x in range(3):
        if ((i - n) < 0) or ((j - n) < 0):
            break
        elif arr[i - n][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


def diag2_check(i, j, color):
    evaluation = 1
    # checks values to the right and up of the point
    m = 1
    for x in range(3):
        if ((i - m) < 0) or ((j + m) > 6):
            break
        elif arr[i - m][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and up of the point
    n = 1
    for x in range(3):
        if ((i + n) > 5) or ((j - n) < 0):
            break
        elif arr[i + n][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


def verticle_check(i, j, color):
    evaluation = 1
    # checks values below the point
    m = 1
    for x in range(3):
        if (i + m) > 5:
            break
        elif arr[i + m][j] == color:
            evaluation += 1
            m += 1
        else:
            break
    return evaluation


def horizontal_check(i, j, color):
    evaluation = 1
    # checks values to the right of the point
    m = 1
    for x in range(3):
        if (j + m) > 6:
            break
        elif arr[i][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left of the point
    n = 1
    for x in range(3):
        if (j - n) < 0:
            break
        elif arr[i][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


def evaluate(color):
    evaluations = np.zeros((7), dtype=int)
    for x in range(7):
        for y in reversed(range(6)):
            if arr[y][x] == 0:
                diagonal1 = diag1_check(y, x, color)
                diagonal2 = diag2_check(y, x, color)
                horizontal = horizontal_check(y, x, color)
                verticle = verticle_check(y, x, color)
                final_eval = max(diagonal1, diagonal2, horizontal, verticle)
                evaluations[x] = final_eval
                break
    return evaluations

red_evaluation = evaluate(-1)
yel_evaluation = evaluate(1)
if max(evaluate(-1) >= 4:
    evaluations(np.max(x, axis=1))

cv2.imshow('cropped', cropped_board)
cv2.waitKey(0)
cv2.destroyAllWindows()
