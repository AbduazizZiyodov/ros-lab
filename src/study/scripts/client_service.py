#!/usr/bin/env python3
import rospy
from study.srv import TemperatureConverter


def temperature_converter_client(celsius: float) -> tuple:
    rospy.wait_for_service("temperature_converter")

    try:
        temperature_converter = rospy.ServiceProxy(
            "temperature_converter", TemperatureConverter
        )
        resp = temperature_converter(celsius)
        return (resp.fahrenheit, resp.kelvin, resp.valid)

    except rospy.ServiceException as e:
        rospy.logerr(f"Bruuh service call failed: {e}")


def main() -> int:
    rospy.init_node("temperature_converter_client")

    for value in (0, 100, -40, 37, -300):
        result = temperature_converter_client(value)
        rospy.loginfo(f"{value=} => {result=}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
