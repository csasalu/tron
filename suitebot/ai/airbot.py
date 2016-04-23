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

# XXX depends on concrete game rules
CRITICAL_HEALTH = 1


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

        # score = profit - cost - risk
        #   cost: number of steps
        #   profit: treasures/batteries obtained on each step
        #   risk: dangers on each step of the move
        #
        # also actions should depend on bot's health: the score of battery
        # should raise if the bot's health is depleating, etc.


        # first valid supplier wins
        move_suppliers = (
            # active avoidance moves (immediate danger,
            # e.g. if we don't go away, we are eaten on next turn)
            # ...
            # NOTE that we don't calc score here, so we don't combine minimized
            # danger with maximized profit!)

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

    def _safe_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_safe_move, SINGLE_MOVES)

    def _is_safe_move(self, move: Move) -> bool:
        move_destination = self._destination(move)
        return move_destination not in self._game_state.get_obstacle_locations()

    def _destination(self, move: Move) -> Point:
        bot_location = self._game_state.get_bot_location(self._bot_id)
        step1_destination = move.step1.destination_from(bot_location)
        if not move.step2:
            return step1_destination
        else:
            return move.step2.destination_from(step1_destination)
