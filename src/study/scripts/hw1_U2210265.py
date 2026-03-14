#!/usr/bin/env python3
import math
import os
import threading

# ros stuff
import rospy
from turtlesim.srv import Kill, SetPen, Spawn, TeleportAbsolute

# font stuff
from rdp import rdp
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from fontPens.flattenPen import FlattenPen


__all__ = ("Turtle",)

COLOR = (255, 255, 255)
WIDTH = 5
SCALE = 3.0
SPACING = 0.20
EPSILON = 0.0001
START_X = 0.5
BASELINE_Y = 4.0
NODE_NAME = "homework-1"
FONT_FILE = "LiberationSans-Regular.ttf"
TARGET_DIGITS = [0, 2, 6, 5]

# Ramer–Douglas–Peucker algorithm was used in order to extract path/segments from font file.
# Outsourced from rdp library, everything is stored in DIGITS global constant(?) below(bottom of this file).
# It should be able to draw anything, even if it is not digit (we're using font file ...).


def main() -> int:
    rospy.init_node(NODE_NAME)

    try:
        rospy.wait_for_service("/kill", timeout=2.0)
        rospy.ServiceProxy("/kill", Kill)("turtle1")
    except Exception:
        pass

    turtles = [Turtle(digit, idx) for idx, digit in enumerate(TARGET_DIGITS)]

    for turtle in turtles:
        turtle.start()

    for turtle in turtles:
        turtle.join()

    return os.EX_OK


class Turtle(threading.Thread):
    """Turtle is just thread with extra methods, sketchy abstraction ..."""

    def __init__(self, digit: int, idx: int) -> None:
        name = f"worker_{idx}"
        super().__init__(name=name)
        self.name = name

        self.spawn()
        self.pen(off=True)

        self.digit, self.idx = digit, idx
        self.width = max(max(p[0] for p in segment) for segment in DIGITS[self.digit])
        self.ox = START_X + self.idx * (self.width + SPACING) * SCALE

    def run(self) -> None:
        self.draw()

    def draw(self) -> None:
        for stroke in DIGITS[self.digit]:
            self.trace(stroke, self.ox, BASELINE_Y, SCALE)
        self.kill()

    def spawn(self) -> None:
        rospy.wait_for_service("/spawn")
        rospy.ServiceProxy("/spawn", Spawn)(0.5, 0.5, 0.0, self.name)

    def kill(self) -> None:
        rospy.wait_for_service("/kill")
        rospy.ServiceProxy("/kill", Kill)(self.name)

    def pen(self, off: bool) -> None:
        rospy.wait_for_service(f"/{self.name}/set_pen")
        rospy.ServiceProxy(f"/{self.name}/set_pen", SetPen)(*COLOR, WIDTH, int(off))

    def teleport(self, x: float, y: float, theta: float) -> None:
        rospy.wait_for_service(f"/{self.name}/teleport_absolute")
        rospy.ServiceProxy(f"/{self.name}/teleport_absolute", TeleportAbsolute)(
            x, y, theta
        )

    def heading(self, a: tuple, b: tuple) -> float:
        return math.atan2(b[1] - a[1], b[0] - a[0])

    def trace(self, stroke: list, ox: float, oy: float, scale: float) -> None:
        points = [(ox + p[0] * scale, oy + p[1] * scale) for p in stroke]

        self.pen(off=True)
        self.teleport(points[0][0], points[0][1], self.heading(points[0], points[1]))
        self.pen(off=False)

        for i in range(1, len(points)):
            self.teleport(
                points[i][0], points[i][1], self.heading(points[i - 1], points[i])
            )

        self.pen(off=True)


def extract_digit_path(digits: list) -> dict:
    font = TTFont(FONT_FILE)
    glyph_set = font.getGlyphSet()
    cmap = font["cmap"].getBestCmap()

    raw_strokes = {}
    min_y, max_y = float("inf"), float("-inf")

    for digit in digits:
        if ord(str(digit)) not in cmap:
            continue

        recorder = RecordingPen()
        glyph_set[cmap[ord(str(digit))]].draw(
            FlattenPen(recorder, approximateSegmentLength=5, segmentLines=True)
        )

        strokes, current_stroke = [], []

        for command, args in recorder.value:
            if command == "moveTo":
                if current_stroke:
                    strokes.append(current_stroke)
                current_stroke = [args[0]]
                min_y = min(min_y, args[0][1])
                max_y = max(max_y, args[0][1])

            elif command == "lineTo":
                current_stroke.append(args[0])
                min_y = min(min_y, args[0][1])
                max_y = max(max_y, args[0][1])

            elif command in ("closePath", "endPath"):
                if current_stroke:
                    if (
                        command == "closePath"
                        and current_stroke[-1] != current_stroke[0]
                    ):
                        current_stroke.append(current_stroke[0])
                    strokes.append(current_stroke)
                    current_stroke = []

        if current_stroke:
            strokes.append(current_stroke)

        raw_strokes[digit] = strokes

    scale = 1.0 / (max_y - min_y) if max_y > min_y else 1.0
    normalized = {}

    for digit, strokes in raw_strokes.items():
        min_x = min((min(p[0] for p in s) for s in strokes if s), default=0)
        normalized[digit] = [
            rdp(
                [((x - min_x) * scale, (y - min_y) * scale) for x, y in stroke], EPSILON
            )
            for stroke in strokes
            if stroke
        ]

    return normalized


DIGITS = extract_digit_path(TARGET_DIGITS)


if __name__ == "__main__":
    raise SystemExit(main())
