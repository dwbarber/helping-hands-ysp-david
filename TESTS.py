import time

import cv2
from nuro_arm import RobotArm
robot = RobotArm()

cam_jpos = [0.00, -1.59174028,  1.03044239, 2.0943951, -0.09215338]
robot.move_arm_jpos(cam_jpos)

cap = cv2.VideoCapture(1)
if not (cap.isOpened()):
    print("Could not open video device")
for i in range(5):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    # cv2.imshow('preview',frame)
    if i ==4:

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
#cropped_board = hsv_img[110:385, 160:513]
cv2.imwrite(name, img)

cv2.imshow('frame', img)
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()