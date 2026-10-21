import time

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from tabulate import tabulate

# As per the assignment, the preset positions are:
positions = [
    {
        "shoulder_pan": 0.0,
        "shoulder_lift": -30.0,
        "elbow_flex": 30.0,
        "wrist_flex": 70.0,
        "wrist_roll": 0.0,
        "gripper": 0.0,
    },
    {
        "shoulder_pan": 45.0,
        "shoulder_lift": -20.0,
        "elbow_flex": 30.0,
        "wrist_flex": 60.0,
        "wrist_roll": -30.0,
        "gripper": 50.0,
    },
    {
        "shoulder_pan": -45.0,
        "shoulder_lift": -10.0,
        "elbow_flex": 0.0,
        "wrist_flex": -30.0,
        "wrist_roll": 30.0,
        "gripper": 30.0,
    },
]


def main():
    # TODO: id?
    robot_config = SO101FollowerConfig(port="/dev/ttyUSB0", id="group5")
    robot = SO101Follower(robot_config)
    robot.connect()

    fmt_dict = lambda pos_dict: "\n" + tabulate(
        [pos_dict], headers="keys", tablefmt="rounded_outline"
    )

    for i, target_pos in enumerate(positions):
        print(
            "\n" + "#" * 100 + f"\nSending position {i}: {fmt_dict(target_pos)}"
        )
        start_time = time.time()
        robot.send_action(target_pos)

        while not positions_within_tolerance(
            robot.get_observation(), target_pos
        ):
            time.sleep(0.05)

        end_time = time.time()

        print(
            f"Actual position after sending position {i}: {fmt_dict(target_pos)}"
        )
        print(
            f"\nTime taken to get to position {i}: {end_time - start_time:.2f} seconds"
        )

        input("Press Enter to continue to the next position...")


def positions_within_tolerance(pos1, pos2, tolerance=1):
    for key in pos1:
        if abs(pos1[key] - pos2[key]) > tolerance:
            return False
    return True


if __name__ == "__main__":
    main()
