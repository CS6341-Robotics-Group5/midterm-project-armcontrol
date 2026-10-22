from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

position = {
    "shoulder_pan.pos": 0.0,
    "shoulder_lift.pos": -30.0,
    "elbow_flex.pos": 30.0,
    "wrist_flex.pos": 70.0,
    "wrist_roll.pos": 0.0,
    "gripper.pos": 0.0,
}


def main():
    robot_config = SO101FollowerConfig(port="/dev/ttyACM0", id="group5")
    robot = SO101Follower(robot_config)
    robot.connect()

    robot.send_action(position)


if __name__ == "__main__":
    main()
