from typing import List

from suitebot.game.game_state import GameState
from suitebot.game.point import Point

OBSTACLE = "*"
TREASURE = "!"
BATTERY = "+"
EMPTY = " "


def create_from_game_plan_lines(game_plan_lines: List[str], bot_energy: int = 10) -> GameState:
    bot_ids = []
    bot_location_map = {}
    bot_energy_map = {}
    obstacles = []
    treasures = []
    batteries = []
    _assert_rectangular_plan(game_plan_lines)
    for (y, line) in enumerate(game_plan_lines):
        for (x, char) in enumerate(line):
            location = Point(x, y)
            if char == OBSTACLE:
                obstacles.append(location)
            elif char == TREASURE:
                treasures.append(location)
            elif char == BATTERY:
                batteries.append(location)
            elif char.isdigit():
                bot_id = int(char)
                bot_ids.append(bot_id)
                bot_location_map[bot_id] = location
                bot_energy_map[bot_id] = bot_energy
            elif char != EMPTY:
                raise ValueError("unrecognized character: %s" % char)
    return GameState(
        plan_width=len(game_plan_lines[0]),
        plan_height=len(game_plan_lines),
        bot_ids=bot_ids,
        bot_location_map=bot_location_map,
        bot_energy_map=bot_energy_map,
        obstacles=obstacles,
        treasures=treasures,
        batteries=batteries
    )


def _assert_rectangular_plan(lines: List[str]) -> None:
    width = len(lines[0])
    for (i, line) in enumerate(lines, start = 1):
        if len(line) != width:
            raise ValueError("non-rectangular plan: line %i width (%i) is different from the line 1 width (%i)" % (
                i, len(line), width))
