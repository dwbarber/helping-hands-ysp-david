import cv2
import numpy as np
import matplotlib.pyplot as plt

# create the cropped image based on downloaded image
img = cv2.imread(r"C:\Users\lowel\Downloads\connect 4.jpg")
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cropped_board = hsv_img[110:550, 0:520]
# cropped_board = img[110:350, 0:520]
shape = cropped_board.shape

# find values that are necessary to access specific pixels
rows = 6
columns = 7

height = shape[0] // rows
width = shape[1] // columns

y1 = (height // 2)
x1 = (width // 2)

# define an array that is the correct size with values that are all zeros
arr = np.zeros([6, 7])


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

        if (h < 30) & (h > 11):
            arr[i][j] = 1

        elif (h < 10) & (h > 0):

            arr[i][j] = -1

        else:
            arr[i][j] = 0

cv2.imshow('cropped', cropped_board)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(arr)
