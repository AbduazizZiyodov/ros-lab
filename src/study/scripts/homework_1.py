#!/usr/bin/env python3

import math
import rospy
import threading
from turtlesim.srv import Spawn, Kill, TeleportAbsolute, SetPen


DIGIT_WIDTH = 1.0
DIGIT_HEIGHT = 1.0
SPACING = 2.0
WIDTH = 20
RGB_COLOR = (255, 255, 255)

SEGMENTS = {
    "a": (0, DIGIT_HEIGHT * 2, DIGIT_WIDTH, DIGIT_HEIGHT * 2),
    "b": (DIGIT_WIDTH, DIGIT_HEIGHT * 2, DIGIT_WIDTH, DIGIT_HEIGHT),
    "c": (DIGIT_WIDTH, DIGIT_HEIGHT, DIGIT_WIDTH, 0),
    "d": (0, 0, DIGIT_WIDTH, 0),
    "e": (0, DIGIT_HEIGHT, 0, 0),
    "f": (0, DIGIT_HEIGHT * 2, 0, DIGIT_HEIGHT),
    "g": (0, DIGIT_HEIGHT, DIGIT_WIDTH, DIGIT_HEIGHT),
}


DIGIT_SEGMENTS = {
    0: ("a", "b", "c", "d", "e", "f"),
    2: ("a", "b", "d", "e", "g"),
    5: ("a", "c", "d", "f", "g"),
    6: ("a", "c", "d", "e", "f", "g"),
}

_turtle_counter: int = 0


def next_turtle_name() -> str:
    global _turtle_counter
    _turtle_counter += 1

    return f"worker_{_turtle_counter}"


def spawn_turtle(name: str, x: float, y: float, theta: float = 0.0) -> None:
    rospy.wait_for_service("/spawn")
    rospy.ServiceProxy("/spawn", Spawn)(x, y, theta, name)


def kill_turtle(name: str) -> None:
    try:
        rospy.wait_for_service("/kill")
        rospy.ServiceProxy("/kill", Kill)(name)
    except Exception as exc:
        rospy.logerr(f"Bruh {exc=}")


def teleport(name: str, x: float, y: float, theta: float) -> None:
    rospy.wait_for_service(f"/{name}/teleport_absolute")
    rospy.ServiceProxy(f"/{name}/teleport_absolute", TeleportAbsolute)(x, y, theta)


def set_pen(name: str, r: int, g: int, b: int, width: int, off: bool) -> None:
    rospy.wait_for_service(f"/{name}/set_pen")
    rospy.ServiceProxy(f"/{name}/set_pen", SetPen)(r, g, b, width, int(off))


def draw_line(
    name: str,
    x1: float,
    y1: float,
    x2: float,
    y2: float
) -> None:
    dx = x2 - x1
    dy = y2 - y1
    theta = math.atan2(dy, dx)

    set_pen(name, *RGB_COLOR, WIDTH, off=True)
    teleport(name, x1, y1, theta)

    set_pen(name, *RGB_COLOR, WIDTH, off=False)
    teleport(name, x2, y2, theta)

    set_pen(name, *RGB_COLOR, WIDTH, off=True)


def draw_digit(digit: int, origin_x: float, origin_y: float) -> None:
    name = next_turtle_name()

    spawn_turtle(name, 1, 1, 0.0)

    segments = DIGIT_SEGMENTS[digit]

    for seg_name in segments:
        x1_rel, y1_rel, x2_rel, y2_rel = SEGMENTS[seg_name]

        draw_line(
            name,
            origin_x + x1_rel,
            origin_y + y1_rel,
            origin_x + x2_rel,
            origin_y + y2_rel,
        )


def draw_digits(digits: list, start_x: float = 2, start_y: float = 5) -> None:
    workers = []

    for i, digit in enumerate(digits):
        workers.append(
            threading.Thread(
                target=draw_digit,
                name=f"worker_{digit}",
                args=(digit, start_x + i * SPACING, start_y),
            )
        )

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()


def finalize_turtles() -> None:
    for idx in range(1, _turtle_counter + 1):
        kill_turtle(f"worker_{idx}")


def main() -> int:
    rospy.init_node("homework_1", anonymous=True)
    kill_turtle("turtle1")
    digits = [0, 2, 6, 5]
    draw_digits(digits)
    finalize_turtles()

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
