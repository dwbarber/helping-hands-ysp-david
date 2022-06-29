from nuro_arm import RobotArm
robot = RobotArm()

run_val = [0.19,0,0.27]
grasp_jpos = [0,-0.255,-1.349,-1.466,0.029]
ee_pos_drop0 = [0.19,0.0381*3, .27]
ee_pos_drop1 = [0.19,0.0381*2,0.27]
ee_pos_drop2 = [0.19,0.0381,0.27]
ee_pos_drop3 = [0.19,0,0.27]
ee_pos_drop4 = [0.19,-0.0381,0.27]
ee_pos_drop5 = [0.19,-0.0381*2,0.27]
ee_pos_drop6 = [0.19,-0.0381*3,0.27]

for i in range(7):
    if i == 0:
        run_val = ee_pos_drop0
    elif i == 1:
        run_val = ee_pos_drop1
    elif i==2:
        run_val == ee_pos_drop2
    elif i == 3:
        run_val == ee_pos_drop3
    elif i == 4:
        run_val == ee_pos_drop4
    elif i== 5:
        run_val == ee_pos_drop5
    else:
        run_val == ee_pos_drop6
    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos)
    robot.close_gripper()
    robot.move_hand_to(run_val)
    robot.open_gripper()
    robot.home()
