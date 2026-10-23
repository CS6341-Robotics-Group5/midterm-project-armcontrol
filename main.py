import time

from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from tabulate import tabulate

# As per the assignment, the preset positions are:
positions = [
    {
        "shoulder_pan.pos": 0.0,
        "shoulder_lift.pos": -30.0,
        "elbow_flex.pos": 30.0,
        "wrist_flex.pos": 70.0,
        "wrist_roll.pos": 0.0,
        "gripper.pos": 0.0,
    },
    {
        "shoulder_pan.pos": 45.0,
        "shoulder_lift.pos": -20.0,
        "elbow_flex.pos": 30.0,
        "wrist_flex.pos": 60.0,
        "wrist_roll.pos": -30.0,
        "gripper.pos": 50.0,
    },
    {
        "shoulder_pan.pos": -45.0,
        "shoulder_lift.pos": -10.0,
        "elbow_flex.pos": 0.0,
        "wrist_flex.pos": -30.0,
        "wrist_roll.pos": 30.0,
        "gripper.pos": 30.0,
    },
]


def main():
    robot_config = SO101FollowerConfig(port="/dev/ttyACM0", id="group5")
    robot = SO101Follower(robot_config)
    robot.connect()

    for i, target_pos in enumerate(positions):
        print("\n" + "#" * 100 + f"\nSending position {i}: {fmt_position(target_pos)}")
        start_time = time.time()
        robot.send_action(target_pos)

        # Wait for the arm to get there
        while not positions_within_tolerance(robot.get_observation(), target_pos, tolerance=2):
            time.sleep(0.05)

        end_time = time.time()

        print(f"Actual position after sending position {i}: {fmt_position(robot.get_observation())}")
        print(f"\nTime taken to get to position {i}: {end_time - start_time:.2f} seconds")

        input("Press Enter to continue to the next position...")

    print("\n" + "#" * 100 + "\nAll positions sent and reached successfully!")


def positions_within_tolerance(pos1, pos2, tolerance=1):
    """
    Check if two position dictionaries are equal (within a certain tolerance of each other).

    @param pos1: First position dictionary
    @param pos2: Second position dictionary
    @param tolerance: Defaults to 1 degree, as per the assignment.
    """
    for key in pos1:
        if abs(pos1[key] - pos2[key]) > tolerance:
            return False
    return True


def fmt_position(pos_dict):
    """
    Print out a position dictionary in a nice table format.
    """
    return "\n" + tabulate([pos_dict], headers="keys", tablefmt="rounded_outline")


if __name__ == "__main__":
    main()
