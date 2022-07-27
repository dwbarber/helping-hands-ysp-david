import cv2
import numpy as np
import keyboard
import time
from nuro_arm import RobotArm
import pickle
import random


def take_pic():  # takes a picture and processes it into an array, returns the array

    # create the cropped image based on camera image
    src = cv2.imread(r"frame.jpg")
    img = cv2.rotate(src, cv2.ROTATE_180)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)


    src = hsv_img
    #undistorted_image = cv2.undistort(src, mtx, dist, None, optimal_camera_matrix)

    cropped_board = src[202:412, 190:500]
    cv2.imshow('frame', cropped_board)
    shape = cropped_board.shape

    # find values that are necessary to access specific pixels
    rows = 6
    columns = 7

    height = shape[0] // rows
    width = shape[1] // columns

    y1 = (height // 2)
    x1 = (width // 2)

    # Take the average hue of a certain range of pixels
    def average_color(i, j):
        y = y1 + (height * i)
        x = x1 + (width * j)
        n = 1
        old_value = 0
        average = 0

        for p in range(5):
            for o in range(5):
                colors = cropped_board[y - 2 + o, x - 2 + p]
                newH = colors[0]
                # newS = colors[1]
                if newH > 75 & newH < 130:
                    average = (newH + old_value) / n
                    n += 1
                    old_value += newH
                cropped_board[y - 2 + o, x - 2 + p] = [0, 0, 0]
    cv2.imshow("p",cropped_board)

take_pic()

# Display the window until any key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()