from nuro_arm import RobotArm
import keyboard as kb
robot = RobotArm()

x = 0.19
y = 0.0381
z = 0.27

run_val = [0.19,0,0.27]
grasp_jpos = [0,-0.255,-1.349,-1.466,0.029]
ee_pos_drop0 = [x,0.0381*3, z]
ee_pos_drop1 = [x,0.0381*2, z]
ee_pos_drop2 = [x,0.0381, z]
ee_pos_drop3 = [x,0,z]
ee_pos_drop4 = [x,-0.0381,z]
ee_pos_drop5 = [x,-0.0381*2,z]
ee_pos_drop6 = [x,-0.0381*3,z]

for i in range(7):
    while True:
        c = input('what column would you like to choose?')

        if c == 1:
            run_val = ee_pos_drop0
        elif c == 2:
            run_val = ee_pos_drop1
        elif c == 3:
            run_val == ee_pos_drop2
        elif c == 4:
            run_val == ee_pos_drop3
        elif c == 5:
            run_val == ee_pos_drop4
        elif c ==6:
            run_val == ee_pos_drop5
        elif c == 7:
            run_val == ee_pos_drop6
        break

    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos)
    robot.close_gripper()
    robot.move_hand_to(run_val)
    robot.open_gripper()
    robot.home()
