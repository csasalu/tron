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
        if height:
            if dest_y < 0:
                # moving above the first row
                dest_y += height
            elif dest_y >= height:
                # moving below last row
                dest_y -= height
        if width:
            if dest_x < 0:
                # moving to the left of the first column
                dest_x += width
            elif dest_x >= width:
                # moving to the right of the last column
                dest_x -= width
        return Point(dest_x, dest_y)

    def __str__(self) -> str:
        return self.name[0].upper()


UP = Direction.up
DOWN = Direction.down
LEFT = Direction.left
RIGHT = Direction.right

ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
