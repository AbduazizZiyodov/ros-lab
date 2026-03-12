#!/usr/bin/env python3
import rospy
from study.srv import (
    TemperatureConverter,
    TemperatureConverterResponse,
    TemperatureConverterRequest,
)


def handle_temperature_converter(
    req: TemperatureConverterRequest,
) -> TemperatureConverterResponse:
    # defaults
    is_valid: bool = True
    fahrenheit = -1
    kelvin = -1

    try:
        celsius = float(req.celcius)
    except Exception as exc:
        rospy.logerr(f"BRUUUH: {exc=}")
        is_valid = False
    else:
        fahrenheit = (celsius * 9 / 5) + 32
        kelvin = celsius + 273.15

    print(f"{celsius=} => {fahrenheit=}F")
    print(f"{celsius=} => {kelvin}K")
    print(f"{is_valid=}")

    return TemperatureConverterResponse(fahrenheit, kelvin, is_valid)


def main() -> None:
    rospy.init_node("add_two_ints_server")

    rospy.Service(
        "temperature_converter", TemperatureConverter, handle_temperature_converter
    )
    rospy.loginfo("Ready convert stuff")
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
