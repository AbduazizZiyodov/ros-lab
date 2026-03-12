#!/usr/bin/env python3
import rospy
import actionlib

from study.msg import NavigateAction, NavigateFeedback, NavigateResult


class NavigationServer:
    def __init__(self) -> None:
        self.server = actionlib.SimpleActionServer(
            "navigate",
            NavigateAction,
            execute_cb=self.execute_callback,
            auto_start=False,
        )
        self.server.start()
        rospy.loginfo("NavigationServer ready.")

    def execute_callback(self, goal) -> None:
        rospy.loginfo(f"Goal received: navigate to {goal.target_pose.pose}")
        feedback = NavigateFeedback()
        result = NavigateResult()

        for i in range(10):
            if self.server.is_preempt_requested():
                rospy.logwarn("Preempt requested — stopping.")
                result.success = False
                result.status_message = "Cancelled by client"
                self.server.set_preempted(result)
                return

            feedback.progress_percentage = float(i * 10)
            feedback.distance_to_goal = 10.0 - float(i)
            feedback.current_status = "Navigating"
            self.server.publish_feedback(feedback)
            rospy.sleep(0.5)

        result.success = True
        result.total_distance = 15.3
        result.status_message = "Goal reached"
        self.server.set_succeeded(result)


def main() -> None:
    rospy.init_node("navigation_server")
    NavigationServer()
    rospy.spin()

    return None


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
