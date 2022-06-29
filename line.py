from nuro_arm import RobotArm
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
    if i == 0:
        run_val = ee_pos_drop0
    elif i == 1:
        run_val = ee_pos_drop1
    elif i == 2:
        run_val == ee_pos_drop2
    elif i == 3:
        run_val == ee_pos_drop3
    elif i == 4:
        run_val == ee_pos_drop4
    elif i == 5:
        run_val == ee_pos_drop5
    else:
        run_val == ee_pos_drop6
    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos)
    robot.close_gripper()
    robot.move_hand_to(run_val)
    robot.open_gripper()
    robot.home()
