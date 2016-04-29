from typing import Iterable

from suitebot.game.point import Point


class Bot:
    def __init__(self, id: int, name: str, segments: Iterable[Point] = None):
        self.id = id
        self.name = name
        self._segments = segments or []
        self.is_alive = False

    def add_segment(self, point: Point):
        self._segments.append(point)

    def get_segments(self) -> Iterable[Point]:
        return self._segments

    def get_location(self) -> Point:
        segments = self.get_segments()
        if segments:
            return segments[-1]
        else:
            return None
