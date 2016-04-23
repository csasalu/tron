from enum import Enum

from suitebot.game.point import Point


class Direction(Enum):
    up = (0, -1)
    down = (0, 1)
    left = (-1, 0)
    right = (1, 0)

    def destination_from(self, source: Point, height: int=None, width: int=None) -> Point:
        dx, dy = self.value
        dest_x = source.x + dx
        dest_y = source.y + dy
        if width and dest_x > width:
            dest_x -= width+1
        if height and dest_y > height:
            dest_y -= height+1
        return Point(dest_x, dest_y)

    def __str__(self) -> str:
        return self.name[0].upper()


UP = Direction.up
DOWN = Direction.down
LEFT = Direction.left
RIGHT = Direction.right

ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
