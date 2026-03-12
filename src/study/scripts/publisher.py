#!/usr/bin/env python3

import rospy
from study.msg import RobotStatus


def main() -> None:
    rospy.init_node("robot_status_publisher")
    pub = rospy.Publisher("/robot_status", RobotStatus, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    battery = 100.0

    while not rospy.is_shutdown():
        msg = RobotStatus()
        msg.robot_name = "RoboBot-1"
        msg.battery_level = battery
        msg.is_moving = True
        msg.error_code = 0

        pub.publish(msg)
        rospy.loginfo(f"Status published — Battery: {battery:.1f}%")

        battery -= 1.0

        if battery < 0:
            battery = 100.0

        rate.sleep()

    return None


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
