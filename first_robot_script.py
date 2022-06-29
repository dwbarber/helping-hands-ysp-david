from nuro_arm import RobotArm

robot = RobotArm()

robot.home()

grasp_jpos = [0.134, 0.8, 0.729, 1.014, 0.008]
mid_jpos = [0.2, 0, 0.5, 0, 0]
drop_jpos = [-0.8, 0.8, 0.729, 1.014, 0.008]

robot.open_gripper()
robot.move_arm_jpos(grasp_jpos)


while True:
    robot.close_gripper()
    gripper_state = robot.get_gripper_state()
    robot.move_arm_jpos(mid_jpos)


    if gripper_state > 0.1:
        robot.move_arm_jpos(drop_jpos)
        robot.open_gripper()
        break

    robot.open_gripper()

robot.home()