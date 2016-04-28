from typing import Iterable, Dict, Tuple, Optional, FrozenSet

from suitebot.game.point import Point


class GameState:
    def __init__(self,
                 plan_width: int,
                 plan_height: int,
                 bot_ids: Iterable[int],
                 bot_location_map: Dict[int, Point],
                 live_bot_ids: Iterable[int] = (),
                 obstacles: Iterable[Point] = ()):
        self._plan_width = plan_width
        self._plan_height = plan_height
        self._bot_ids = tuple(bot_ids)
        self._live_bot_ids = frozenset(live_bot_ids if live_bot_ids else bot_ids)
        self._bot_location_map = dict(bot_location_map.items())
        self._obstacles = frozenset(obstacles)

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

    def get_all_bot_ids(self) -> Tuple[int]:
        """Returns the list of the IDs of all bots, including the dead ones.

        :return the list of the IDs of all bots
        """
        return self._bot_ids

    def get_live_bot_ids(self) -> FrozenSet[int]:
        """Returns the set of the IDS of all live bots, i.e. the bots that are still active in the game.

        :return the set of the IDS of all live bots
        """
        return self._live_bot_ids

    def get_bot_location(self, bot_id: int) -> Optional[Point]:
        """Returns the coordinates of the location of the bot on the game plan.

        :param bot_id: ID of the bot
        :return the location of the bot or None if the bot is dead
        :raises ValueError: if the bot ID is unknown
        """
        self._assert_known_bot(bot_id)
        return self._bot_location_map.get(bot_id)

    def get_obstacle_locations(self) -> FrozenSet[Point]:
        """Returns the set of coordinates of all obstacles on the game plan.

        :return the set of coordinates of all obstacles
        """
        return self._obstacles

    def _assert_known_bot(self, bot_id: int) -> None:
        if bot_id not in self._bot_ids:
            raise ValueError("uknown bot ID: %i" % bot_id)
