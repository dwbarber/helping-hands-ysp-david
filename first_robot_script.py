from nuro_arm import RobotArm

robot = RobotArm()

robot.home()

grasp_jpos = [0,-0.255,-1.349,-1.466,0.029]
mid_jpos = [0.2, 0, 0.5, 0, 0]
drop_jpos = [0, -0.125, 0.724, 0.98, 0]

for i in range(3):
    robot.open_gripper()
    robot.move_arm_jpos(grasp_jpos)
    achieved_grasp_jpos = robot.get_arm_jpos()
    print(achieved_grasp_jpos)
    robot.close_gripper()
    robot.move_arm_jpos(drop_jpos)
    robot.open_gripper()

robot.home()
