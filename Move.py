import time
from nuro_arm import RobotArm
import numpy as np


robot = RobotArm()
robot.passive_mode()
amount = 50
x=0
arr = np.zeros([amount,5])

for i in range(amount):
    bot_pos = robot.get_arm_jpos()
    bas = bot_pos[0]
    sho = bot_pos[1]
    elb = bot_pos[2]
    wri = bot_pos[3]
    wrirot = bot_pos[4]
    arr[x] = [bas, sho, elb,wri,wrirot]
    time.sleep(0.1)
    x += 1

time.sleep(2)
robot.active_mode()

for i in range(amount):
    drop_pos = arr[i]
    robot.move_arm_jpos(drop_pos)

