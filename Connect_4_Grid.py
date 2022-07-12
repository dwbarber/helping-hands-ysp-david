import cv2
import numpy as np
import matplotlib.pyplot as plt

# create the cropped image based on downloaded image
img = cv2.imread(r"C:\Users\lowel\Downloads\connect 4.jpg")
cropped_board = img[110:550, 0:520]
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

# upload values to the array
# **opencv Interprets colors in BGR and Matplotlib is in RGB**
for i in range(rows):
    for j in range(columns):
        y = y1 + (height * i)
        x = x1 + (width * j)
        colors = cropped_board[y, x]

        if ((colors[2] < 255) & (colors[2] > 230)) & ((colors[1] < 230) & (colors[1] > 200)) & ((colors[0] < 20)):
            arr[i][j] = 1

        elif ((colors[2] < 255) & (colors[2] > 230)) & ((colors[1] < 100) & (colors[1] > 40)) & ((colors[0] < 20)):
            arr[i][j] = -1

        else:
            arr[i][j] = 0
        cropped_board[y, x] = [255, 255, 255]


print(arr)
# print(cropped_board[-10,-37])
# print(len(cropped_board))
# print(x1,y1,height,width)


def diag1_check(i, j):
    evaluation = 1
    # checks values to the right and down of the point
    m = 1
    for x in range(3):
        if ((i + m) > 5) or ((j + m) > 6):
            break
        elif (arr[i + m][j + m] == 1):
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and up of the point
    n = 1
    for x in range(3):
        if ((i - n) < 0) or ((j - n) < 0):
            break
        elif (arr[i - n][j - n] == 1):
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


def diag2_check(i, j):
    evaluation = 1
    # checks values to the right and up of the point
    m = 1
    for x in range(3):
        if ((i + m) < 0) or ((j + m) > 6):
            break
        elif (arr[i - m][j + m] == 1):
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and up of the point
    n = 1
    for x in range(3):
        if ((i - n) > 0) or ((j - n) < 0):
            break
        elif (arr[i + n][j - n] == 1):
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


def verticle_check(i, j):
    evaluation = 1
    # checks values below the point
    m = 1
    for x in range(3):
        if (i + m) > 5:
            break
        elif (arr[i + m][j] == 1):
            evaluation += 1
            m += 1
        else:
            break
    return evaluation


def horizontal_check(i, j):
    evaluation = 1
    # checks values to the right of the point
    m = 1
    for x in range(3):
        if (arr[i][j + m] == 1):
            if (j + m) > 5:
                break
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left of the point
    n = 1
    for x in range(3):
        if (arr[i][j - n] == 1):
            if (j - n) < 0:
                break
            evaluation += 1
            n += 1
        else:
            break
    return evaluation


evaluations = np.zeros((7), dtype=int)
for x in range(7):
    for y in reversed(range(6)):
        if (arr[y][x] == 0):
            Diagonal1 = diag1_check(y, x)
            #Diagonal2 = diag2_check(y, x)
            #horizontal = horizontal_check(y, x)
            #verticle = verticle_check(y, x)
            #final_eval = max(Diagonal1, Diagonal2, horizontal, verticle)
            #evaluations[j] = final_eval
            print(Diagonal1)
            break




cv2.imshow('cropped', cropped_board)
cv2.waitKey(0)
cv2.destroyAllWindows()
