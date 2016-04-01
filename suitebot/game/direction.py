from enum import Enum

from suitebot.game.point import Point


class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    def destination_from(self, source: Point) -> Point:
        dx, dy = self.value
        return Point(source.x + dx, source.y + dy)

    def __str__(self) -> str:
        return self.name[0].upper()


UP = Direction.up
DOWN = Direction.down
LEFT = Direction.left
RIGHT = Direction.right

ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
