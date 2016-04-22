import itertools
from typing import Iterator

from suitebot.ai.bot_ai import BotAi
from suitebot.game.direction import ALL_DIRECTIONS, UP, DOWN, LEFT, RIGHT
from suitebot.game.game_state import GameState
from suitebot.game.move import Move
from suitebot.game.point import Point

BOT_NAME = 'Airbot'

DEFAULT_MOVE = Move(DOWN)

SINGLE_MOVES = tuple([Move(d) for d in ALL_DIRECTIONS])
DOUBLE_MOVES = tuple([Move(d1, d2) for (d1, d2) in itertools.product(ALL_DIRECTIONS, ALL_DIRECTIONS)])


class Airbot(BotAi):
    """OpenAir team's bot AI.  Based off SampleBot AI."""

    _bot_id = None  # type: int
    _game_state = None  # type: GameState

    def make_move(self, bot_id: int, game_state: GameState) -> Move:
        """If a treasure is close (distance 1), go to it;
        otherwise, if a battery is close, go to it;
        otherwise, if a treasure is reachable (distance 2), go to it;
        otherwise, if a battery is reachable, go to it;
        otherwise, if a safe move can be made (one that avoids any obstacles), do it;
        otherwise, go down.
        """
        self._bot_id = bot_id
        self._game_state = game_state
        if self._is_dead():
            return DEFAULT_MOVE

        # first valid supplier wins
        move_suppliers = (
            # active avoidance moves (immediate danger,
            # e.g. if we don't go away, we are eaten on next turn)
            # ...
            # NOTE that we don't calc score here, so we don't combine minimized
            # danger with maximized profit!)

            # profitable one-step moves (no danger, following best immediate profit)
            self._close_treasure_move_supplier,
            self._close_battery_move_supplier,

            # profitable two-step moves (no danger, following best remote profit)
            self._reachable_treasure_move_supplier,
            self._reachable_battery_move_supplier,

            # passive avoidance moves (no profit, no danger, just moving around obstacles)
            self._safe_move_supplier,
        )
        for move_supplier in move_suppliers:
            try:
                return next(move_supplier())
            except StopIteration:
                continue
        return DEFAULT_MOVE

    def get_name(self) -> str:
        return BOT_NAME

    def _is_dead(self) -> bool:
        return self._bot_id not in self._game_state.get_live_bot_ids()

    def _close_treasure_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_move_to_treasure, SINGLE_MOVES)

    def _close_battery_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_move_to_battery, SINGLE_MOVES)

    def _reachable_treasure_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_move_to_treasure, DOUBLE_MOVES)

    def _reachable_battery_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_move_to_battery, DOUBLE_MOVES)

    def _safe_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_safe_move, SINGLE_MOVES)

    def _is_move_to_treasure(self, move: Move) -> bool:
        move_destination = self._destination(move)
        return move_destination in self._game_state.get_treasure_locations()

    def _is_move_to_battery(self, move: Move) -> bool:
        move_destination = self._destination(move)
        return move_destination in self._game_state.get_battery_locations()

    def _is_safe_move(self, move: Move) -> bool:
        move_destination = self._destination(move)
        if not self._is_destination_within_plan_boundaries(move_destination):
            return False
        return move_destination not in self._game_state.get_obstacle_locations()

    def _is_destination_within_plan_boundaries(self, destination: Point) -> bool:
        horizontal_ok = 0 <= destination.x < self._game_state.get_plan_width()
        vertical_ok   = 0 <= destination.y < self._game_state.get_plan_height()
        return horizontal_ok and vertical_ok

    def _destination(self, move: Move) -> Point:
        bot_location = self._game_state.get_bot_location(self._bot_id)
        step1_destination = move.step1.destination_from(bot_location)
        if not move.step2:
            return step1_destination
        else:
            return move.step2.destination_from(step1_destination)
