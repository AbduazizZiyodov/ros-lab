#!/usr/bin/env python3


###
# WIP
###

import rospy
import typing as t
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.srv import Kill

import random

TURTLE_COUNT: "t.Final[int]" = 4
INDICES: "tuple[int]" = tuple(range(1, TURTLE_COUNT + 1))


def clear():
    rospy.wait_for_service("/kill")
    try:
        kill_turtle = rospy.ServiceProxy("/kill", Kill)
        for idx in INDICES:
            kill_turtle(f"turtle{idx}")
    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")


def create_turtle(turtle_x, turtle_y, turtle_theta, turtle_name):
    rospy.wait_for_service("spawn")
    spawner = rospy.ServiceProxy("spawn", Spawn)
    spawner(turtle_x, turtle_y, turtle_theta, turtle_name)


def move_turtles_random():
    publishers = (
        rospy.Publisher(f"/turtle{idx}/cmd_vel", Twist, queue_size=10)
        for idx in INDICES
    )

    v_pub1 = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size=10)
    v_pub2 = rospy.Publisher("/turtle3/cmd_vel", Twist, queue_size=10)

    rate = rospy.Rate(10)

    vel1, vel2 = Twist(), Twist()

    del_t = 1

    while not rospy.is_shutdown():
        if del_t % 5 == 0:
            vel1.linear.x = random.uniform(0, 3)
            vel1.angular.z = random.uniform(-2, 2)
            vel2.linear.x = random.uniform(0, 3)
            vel2.angular.z = random.uniform(-2, 2)

        v_pub1.publish(vel1)
        v_pub2.publish(vel2)

        del_t += 1

        rate.sleep()


def main() -> int:
    try:
        rospy.init_node("turtle_spawner")

        clear()
        create_turtle(1, 1, 0, "turtle1")
        create_turtle(9, 9, 0, "turtle2")
        create_turtle(1, 1, 0, "turtle3")
        create_turtle(9, 9, 0, "turtle4")

        move_turtles_random()

    except rospy.ROSInterruptException:
        pass


if __name__ == "__main__":
    raise SystemExit(main())
