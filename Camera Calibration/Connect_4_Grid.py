import cv2
import numpy as np
import keyboard
import time
from nuro_arm import RobotArm
import pickle
import random

robot = RobotArm()
cam_jpos = [0.00, -1.59174028,  1.03044239, 2.0943951, -0.09215338]


def simple_ai():
    robot.move_arm_jpos(cam_jpos)

    cap = cv2.VideoCapture(1)
    if not (cap.isOpened()):
        print("Could not open video device")
    for i in range(5):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        # cv2.imshow('preview',frame)
        if i == 4:

            # Waits for a user input to quit the application
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            name = 'frame.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
        time.sleep(0.2)

    # create the cropped image based on camera image
    src = cv2.imread(r"frame.jpg")
    img = cv2.rotate(src, cv2.ROTATE_180)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # cropped_board = hsv_img[110:550, 0:520]
    # cropped_board = hsv_img[110:385, 160:513]

    calib_result_pickle = pickle.load(open("camera_calib_pickle.p", "rb"))
    mtx = calib_result_pickle["mtx"]
    optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
    dist = calib_result_pickle["dist"]

    # create the cropped image based on camera image r'C:\Users\lowel\OneDrive\Pictures\cameraCal\img0.jpg'
    src = hsv_img
    # distorted_image = cv2.rotate(src, cv2.ROTATE_180)
    undistorted_image = cv2.undistort(src, mtx, dist, None, optimal_camera_matrix)

    cropped_board = undistorted_image[202:412, 190:500]
    cv2.imshow('frame', cropped_board)
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
                cropped_board[y - 2 + o, x - 2 + p] = [0, 0, 100]
        return average

    # upload values to the array
    # **opencv Interprets colors in BGR and Matplotlib is in RGB**
    for i in range(rows):
        for j in range(columns):
            h = average_color(i, j)

            if (85 < h) & (h < 96):
                arr[i][j] = 1

            elif (110 < h) & (h < 130):

                arr[i][j] = -1

            else:
                arr[i][j] = 0
            print(i, j, h)

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

    print(yel_evaluation)

    if max(red_evaluation) >= 4:  # checks to see if
        result = np.where(red_evaluation == np.amax(red_evaluation))
        column = int(result[0])
    else:
        result = np.where(yel_evaluation == np.amax(yel_evaluation))
        if len(result) % 2 == 0:
            n = random.randint(int(len(result)/2 - 1), int(len(result)/2))
            column = int(result[n])
        else:
            column = int(np.median(result))
    print(result)
    print(column)

    x = 0.19
    y = 0.0381
    z = 0.3

    run_val = [0.19, 0, 0.27]
    grasp_jpos = [0, -0.255, -1.349, -1.466, 0.029]
    ee_pos_drop0 = [x, 0.1143, z]
    ee_pos_drop1 = [x, 0.0762, z]
    ee_pos_drop2 = [x, 0.0381, z]
    ee_pos_drop3 = [x, 0, z]
    ee_pos_drop4 = [x, -0.0381, z]
    ee_pos_drop5 = [x, -0.0762, z]
    ee_pos_drop6 = [x, -0.1143, z]

    eepos = [ee_pos_drop0, ee_pos_drop1, ee_pos_drop2, ee_pos_drop3, ee_pos_drop4, ee_pos_drop5, ee_pos_drop6]

    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos)
    robot.close_gripper()
    robot.move_hand_to(eepos[column])
    robot.open_gripper()
    robot.home()

    # cv2.imshow('cropped', cropped_board)
    # .waitKey(0)
    # cv2.destroyAllWindows()


for i in range(20):
    keyboard.wait('esc')
    simple_ai()
