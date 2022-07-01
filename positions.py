import time
from nuro_arm import RobotArm
robot = RobotArm()
import matplotlib.pyplot as plt
import numpy as np

robot.passive_mode()

bot_pos = robot.get_arm_jpos()
x=0

arr = np.array([0,0,0,0,0,0])
arr2d = arr.reshape(5,1)

for i in range(10):
    x += 1
    bas = bot_pos[0]
    sho = bot_pos[1]
    elb = bot_pos[2]
    wri = bot_pos[3]
    wrirot = bot_pos[4]
    np.append(arr2d, [[x,bas,sho,elb,wri,wrirot]], axis=0)
    time.sleep(0.2)

plt.scatter(arr2d[0], arr2d[1])
plt.title('Base Positions')
plt.xlabel('Time (S)')
plt.ylabel('Servo Value')

