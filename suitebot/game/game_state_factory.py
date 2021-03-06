from typing import List

from suitebot.game.game_state import GameState
from suitebot.game.point import Point
from suitebot.game.bot import Bot

OBSTACLE = "*"
EMPTY = " "


def create_from_game_plan_lines(game_plan_lines: List[str]) -> GameState:
    bot_ids = []
    bot_location_map = {}
    obstacles = []
    _assert_rectangular_plan(game_plan_lines)
    for (y, line) in enumerate(game_plan_lines):
        for (x, char) in enumerate(line):
            location = Point(x, y)
            if char == OBSTACLE:
                obstacles.append(location)
            elif char.isdigit():
                bot_id = int(char)
                bot_ids.append(bot_id)
                bot_location_map[bot_id] = location
            elif char != EMPTY:
                raise ValueError("unrecognized character: %s" % char)

    bots = {}

    # add bots
    for bot_id in bot_ids:
        bot = Bot(id=bot_id, name='Bot #{}'.format(bot_id))
        if bot_id in bot_location_map:
            location = bot_location_map[bot_id]
            bot.add_segment(location)
        bots[bot_id] = bot

    return GameState(
        plan_width=len(game_plan_lines[0]),
        plan_height=len(game_plan_lines),
        bots=bots,
        obstacles=obstacles,
    )


def _assert_rectangular_plan(lines: List[str]) -> None:
    width = len(lines[0])
    for (i, line) in enumerate(lines, start = 1):
        if len(line) != width:
            raise ValueError("non-rectangular plan: line %i width (%i) is different from the line 1 width (%i)" % (
                i, len(line), width))
