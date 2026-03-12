#!/usr/bin/env python3
import rospy
import actionlib

from study.msg import NavigateAction, NavigateGoal


def feedback_callback(feedback) -> None:
    rospy.loginfo(
        f"Progress: {feedback.progress_percentage:.1f}%  "
        f"Distance: {feedback.distance_to_goal:.2f} m  "
        f"Status: {feedback.current_status}"
    )


def main() -> int:
    rospy.init_node("navigation_client")

    client = actionlib.SimpleActionClient("navigate", NavigateAction)
    rospy.loginfo("Waiting for action server...")
    client.wait_for_server()

    goal = NavigateGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = 5.0
    goal.target_pose.pose.position.y = 3.0
    goal.max_speed = 0.5
    goal.avoid_obstacles = True

    client.send_goal(goal, feedback_cb=feedback_callback)
    rospy.loginfo("Goal sent - waiting for result...")

    client.wait_for_result(rospy.Duration(60.0))

    result = client.get_result()
    state = client.get_state()
    rospy.loginfo(
        f"State: {state}  Success: {result.success}  "
        f"Distance: {result.total_distance:.1f}m"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
