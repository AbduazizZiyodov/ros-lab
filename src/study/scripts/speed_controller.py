#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


def main() -> int:
    rospy.init_node("speed_controller")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

    rospy.set_param("/turtle_speed", 1.0)

    rate = rospy.Rate(hz=10)

    while not rospy.is_shutdown():
        speed = rospy.get_param("/turtle_speed", 1.0)
        msg = Twist()
        msg.linear.x = speed
        pub.publish(msg)

        rate.sleep()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
