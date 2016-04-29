from typing import Iterable, Dict, Tuple, Optional, FrozenSet

from suitebot.game.point import Point
from suitebot.game.bot import Bot


class GameState:
    def __init__(self,
                 plan_width: int,
                 plan_height: int,
                 bots: Dict[int, Bot],
                 obstacles: Iterable[Point] = ()):

        self._plan_width = plan_width
        self._plan_height = plan_height

        self._bots = bots

        self._static_obstacles = frozenset(obstacles)

    def get_plan_width(self) -> int:
        """Returns the width of the game plan.

        :return the width of the game plan
        """
        return self._plan_width

    def get_plan_height(self) -> int:
        """Returns the height of the game plan.

        :return the height  of the game plan
        """
        return self._plan_height

    def get_bots(self) -> Iterable[Bot]:
        return self._bots.values()

    def get_bot(self, id: int) -> Bot:
        return self._bots[id]

    def get_all_bot_ids(self) -> Tuple[int]:
        """Returns the list of the IDs of all bots, including the dead ones.

        :return the list of the IDs of all bots
        """
        return frozenset(self._bots.keys())

    def get_live_bot_ids(self) -> FrozenSet[int]:
        """Returns the set of the IDS of all live bots, i.e. the bots that are still active in the game.

        :return the set of the IDS of all live bots
        """
        return {bot.id for bot in self.get_bots() if bot.is_alive}

    def get_bot_location(self, bot_id: int) -> Optional[Point]:
        """Returns the coordinates of the location of the bot on the game plan.

        :param bot_id: ID of the bot
        :return the location of the bot or None if the bot is dead
        :raises ValueError: if the bot ID is unknown
        """
        return self.get_bot(bot_id).get_location()

    def _generate_obstacle_locations(self) -> Iterable[Point]:
        for obstacle in self._static_obstacles:
            yield obstacle
        for bot in self.get_bots():
            for segment in bot.get_segments():
                yield segment

    def get_obstacle_locations(self) -> FrozenSet[Point]:
        """Returns the set of coordinates of all obstacles on the game plan.

        :return the set of coordinates of all obstacles
        """
        return set(self._generate_obstacle_locations())

    def _assert_known_bot(self, bot_id: int) -> None:
        if bot_id not in self._bots:
            raise ValueError("uknown bot ID: %i" % bot_id)
