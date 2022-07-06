import time
from nuro_arm import RobotArm
robot = RobotArm()
import matplotlib.pyplot as plt
import numpy as np

robot.passive_mode()
x=0
arr = np.zeros([10,6])

for i in range(10):
    bot_pos = robot.get_arm_jpos()
    bas = bot_pos[0]
    sho = bot_pos[1]
    elb = bot_pos[2]
    wri = bot_pos[3]
    wrirot = bot_pos[4]
    arr[x] = [x, bas, sho, elb,wri,wrirot]
    time.sleep(0.2)
    x += 1


print(arr)
plt.scatter(arr[:,0],arr[:,1])
plt.scatter(arr[:,0],arr[:,2])
plt.scatter(arr[:,0],arr[:,3])
plt.scatter(arr[:,0],arr[:,4])
plt.scatter(arr[:,0],arr[:,5])
plt.show()


