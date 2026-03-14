#!/usr/bin/env python3


###
# WIP
###

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.srv import Kill

import random

TURTLE_COUNT = 4
INDICES = tuple(range(1, TURTLE_COUNT + 1))
INITIAL_COORDINATES = (
    (2,                   5.5, 10.0),
    (2 + 2.5,             5.5, 10.0),
    (2 + 2.5 + 2.5,       5.5, 10.0),
    (2 + 2.5 + 2.5 + 2.5, 5.5, 10.0),
)


def main() -> int:
    try:
        rospy.init_node("turtle_spawner")
        kill_existing_turtles()
        initialize_turtles()
        # move_turtles_random()
    except rospy.ROSInterruptException:
        pass

    return 0


def kill_existing_turtles() -> None:
    rospy.wait_for_service("/kill")
    kill_turtle = rospy.ServiceProxy("/kill", Kill)

    try:
        for idx in INDICES:
            kill_turtle(f"turtle{idx}")
    except rospy.ServiceException as exc:
        print(f"Service call failed: {exc}")


def create_turtle(turtle_x, turtle_y, turtle_theta, turtle_name) -> None:
    rospy.wait_for_service("spawn")
    spawner = rospy.ServiceProxy("spawn", Spawn)
    spawner(turtle_x, turtle_y, turtle_theta, turtle_name)

def move_turtles_random() -> None:
    publishers = tuple(
        rospy.Publisher(f"/turtle{idx}/cmd_vel", Twist, queue_size=10)
        for idx in INDICES
    )

    rate = rospy.Rate(10)
    velocities = tuple(Twist() for _ in INDICES)

    while not rospy.is_shutdown():
        for vel in velocities:
            vel.angular.z = 1
            vel.linear.x = 1

        for v_pub, vel in zip(publishers, velocities):
            v_pub.publish(vel)

        rate.sleep()


def initialize_turtles() -> None:
    for idx, coordinate in zip(INDICES, INITIAL_COORDINATES):
        create_turtle(*coordinate, f"turtle{idx}")


if __name__ == "__main__":
    raise SystemExit(main())
