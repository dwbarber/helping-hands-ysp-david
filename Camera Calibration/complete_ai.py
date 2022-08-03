import cv2
import numpy as np
import keyboard
import time
import random
from nuro_arm import RobotArm
import pickle


def take_pic():  # takes a picture and processes it into an array, returns the array
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

    # undistort the image using values from calibration
    calib_result_pickle = pickle.load(open("camera_calib_pickle.p", "rb"))
    mtx = calib_result_pickle["mtx"]
    optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
    dist = calib_result_pickle["dist"]

    src = hsv_img
    undistorted_image = cv2.undistort(src, mtx, dist, None, optimal_camera_matrix)

    cropped_board = undistorted_image[192:405, 175:485]
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
                if newH > 75 & newH < 130:
                    average = (newH + old_value) / n
                    n += 1
                    old_value += newH
                cropped_board[y - 2 + o, x - 2 + p] = [0, 0, 100]
        cv2.imwrite(name, cropped_board)
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
            # print(i, j, h)
    return arr


def diag1_check(i, j, color, layout):
    evaluation = 1
    # checks values to the right and down of the point
    m = 1
    for x in range(3):
        if ((i + m) > 5) or ((j + m) > 6):
            break
        elif layout[i + m][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and up of the point
    n = 1
    for x in range(3):
        if ((i - n) < 0) or ((j - n) < 0):
            break
        elif layout[i - n][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    if evaluation >= 4:
        evaluation = 1000
    evaluation = color * evaluation
    return evaluation


def diag2_check(i, j, color, layout):
    evaluation = 1
    # checks values to the right and up of the point
    m = 1
    for x in range(3):
        if ((i - m) < 0) or ((j + m) > 6):
            break
        elif layout[i - m][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left and down of the point
    n = 1
    for x in range(3):
        if ((i + n) > 5) or ((j - n) < 0):
            break
        elif layout[i + n][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    if evaluation >= 4:
        evaluation = 1000
    evaluation = color * evaluation
    return evaluation


def vertical_check(i, j, color, layout):
    evaluation = 1
    # checks values below the point
    m = 1
    for x in range(3):
        if (i + m) > 5:
            break
        elif layout[i + m][j] == color:
            evaluation += 1
            m += 1
            # ("eval down", evaluation)
        else:
            break
    n = 1
    # checks values above the point
    for x in range(3):
        if (i - n) < 0:
            break
        elif layout[i - n][j] == color:
            evaluation += 1
            n += 1
            # print("eval up", evaluation)
        else:
            break
    if evaluation >= 4:
        evaluation = 1000
    evaluation = color * evaluation
    return evaluation


def horizontal_check(i, j, color, layout):
    evaluation = 1
    # checks values to the right of the point
    m = 1
    for x in range(3):
        if (j + m) > 6:
            break
        elif layout[i][j + m] == color:
            evaluation += 1
            m += 1
        else:
            break
    # checks values to the left of the point
    n = 1
    for x in range(3):
        if (j - n) < 0:
            break
        elif layout[i][j - n] == color:
            evaluation += 1
            n += 1
        else:
            break
    if evaluation >= 4:
        evaluation = 1000
    evaluation = color * evaluation
    return evaluation


def evaluate(color, layout):
    evaluations = []
    for y in range(6):
        for x in range(7):
            if layout[y][x] == color:
                diagonal1 = diag1_check(y, x, color, layout)
                diagonal2 = diag2_check(y, x, color, layout)
                horizontal = horizontal_check(y, x, color, layout)
                vertical = vertical_check(y, x, color, layout)
                if color == 1:
                    point_eval = max(diagonal1, diagonal2, horizontal, vertical)
                    evaluations.append(point_eval)
                elif color == -1:
                    point_eval = min(diagonal1, diagonal2, horizontal, vertical)
                    evaluations.append(point_eval)
    return evaluations


def score(depth, layout):
    offense_factor = 1
    defense_factor = 1
    return offense_factor * max([*evaluate(1, layout),0]) + defense_factor * min([*evaluate(-1, layout),0])


def valid_positions(layout):
    array = []
    for i in range(7):
        if layout[0][i] == 0:
            array.append(i)
    return array


def create_hypoboard(depth, layout, col):
    color = 1
    if depth % 2 == 1:
        color = -1
    row = np.where(layout[:, col] == 0)[0][-1]
    hypo = layout.copy()
    hypo[row, col] = color
    return hypo


def minmax(max_depth, depth, layout):
    scores_list = []
    vps = valid_positions(layout)
    current_score = score(depth, layout)
    if abs(current_score) > 50:
        return current_score
    if depth == max_depth:
        return current_score
    else:
        for vp in vps:
            new_hypoboard = create_hypoboard(depth, layout, vp)
            scores_list.append(minmax(max_depth, depth + 1, new_hypoboard))
        if depth % 2 == 0:
            return max(scores_list)
        else:
            return min(scores_list)


def determine_action(max_depth, layout):
    action_scores = []
    valid_pos = np.array(valid_positions(layout))
    for col in valid_pos:
        new_hypoboard = create_hypoboard(0, layout, col)
        action_scores.append(minmax(max_depth, 1, new_hypoboard))
    print('action_scores', action_scores)
    print('max', max(action_scores))
    bestaction = np.where(np.asarray(action_scores) == max(action_scores))[0]
    print()
    print(bestaction)
    prob = 1/(abs(valid_pos[bestaction] - 3) + 0.5)**0.5
    n = np.random.choice(bestaction, p=prob/prob.sum())
    return valid_pos[n]


def move(column):
    x = 0.15
    y = 0.0381
    z = 0.33

    run_val = [0.19, 0, 0.27]
    grasp_jpos = [0, -0.255, -1.4, -1.5, 0.029]
    ee_pos_drop0 = [x, 0.0950, z]
    ee_pos_drop1 = [x, 0.068, z]
    ee_pos_drop2 = [x, 0.0381, z]
    ee_pos_drop3 = [x, 0, z]
    ee_pos_drop4 = [x, -0.0381, z]
    ee_pos_drop5 = [x, -0.068, z]
    ee_pos_drop6 = [x, -0.0950, z]
    eepos = [ee_pos_drop0, ee_pos_drop1, ee_pos_drop2, ee_pos_drop3, ee_pos_drop4, ee_pos_drop5, ee_pos_drop6]

    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos, 1.7)
    robot.close_gripper()
    robot.move_hand_to(eepos[column], speed=1.7)
    robot.open_gripper()
    robot.home()

    # cv2.imshow('cropped', cropped_board)
    # .waitKey(0)
    # cv2.destroyAllWindows()


# board = np.array([[ 0,  0,  0,  0 , 0 , 0 , 0],
#                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0],
#                 [ 0,  0 , 0 , 0 , 0 , 0 , 0],
#                 [ 0 , 0 , 0 , 0 , 0 , 0 , 0],
#                 [ 0 , 0 , 1 , 1 , 0 , 0 , 0],
#                 [ 1,  1 , -1 , -1 ,-1 , 1 , 0]])


for i in range(20):
    robot = RobotArm()
    cam_jpos = [0.00, -1.59174028, 1.03044239, 2.0943951, 0.0]
    # define an array that is the size of the board with values that are all zeros
    arr = np.zeros([6, 7], dtype=int)
    keyboard.wait('esc')
    print("calculating...")
    board = take_pic()
    pick = determine_action(4, board)
    print('column', pick)
    move(pick)
    robot.move_arm_jpos(cam_jpos,1.7)
