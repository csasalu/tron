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

NOOK_PENALTY = -100
COLLISION_PENALTY = -200


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
            self._safe_move_supplier,
        )
        move_score_calculators = (
            self._nook_risk_calculator,
            self._collision_risk_calculator,
        )
        for move_supplier in move_suppliers:
            try:
                supplied_moves = list(move_supplier())
                if not supplied_moves:
                    continue
                scored_moves = []
                for move in supplied_moves:
                    score = 0.0
                    for score_calculator in move_score_calculators:
                        score += score_calculator(move)
                    scored_moves.append(
                        {
                            'move': move,
                            'score': score,
                        }
                    )
                sorted_moves = list(sorted(scored_moves, key=lambda elem: elem['score']))
                best_move = sorted_moves[-1]['move']
                return best_move
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
        is_not_obstacle = move_destination not in self._game_state.get_obstacle_locations()
        return is_not_obstacle #and is_not_nook and is_not_collision_risk

    def _nook_risk_calculator(self, move: Move) -> float:
        if self._is_not_nook(move):
            return 0
        else:
            return NOOK_PENALTY

    def _collision_risk_calculator(self, move: Move) -> float:
        if self._is_move_safe_from_enemies(move):
            return 0
        else:
            return COLLISION_PENALTY

    def _is_not_nook(self, move: Move) -> bool:
        move_destination = self._destination(move)
        # after the move there should be no other safe moves (or just one
        # because we don't count our tail from current state)
        cnt = 0
        for dest in ALL_DIRECTIONS:
            possible_dest = dest.destination_from(move_destination,
                                  height=self._game_state.get_plan_height(),
                                  width=self._game_state.get_plan_width())
            if possible_dest in self._game_state.get_obstacle_locations():
                cnt += 1
        if cnt >= 3:
            return False
        return True

    def _is_move_safe_from_enemies(self, move: Move) -> bool:
        move_destination = self._destination(move)
        return self._is_clear_from_enemies(move_destination)

    def _is_clear_from_enemies(self, point: Point) -> bool:
        cnt = 0
        all_bot_locations = [
            self._game_state.get_bot_location(b)
            for b in self._game_state.get_live_bot_ids()
            if b != self._bot_id
        ]
        for direction in ALL_DIRECTIONS:
            # actually we check if, getting to that point, we get into the move
            # zone of an enemy, i.e. if it's adjacent to that point
            adjacent_square = direction.destination_from(point,
                                  height=self._game_state.get_plan_height(),
                                  width=self._game_state.get_plan_width())
            if adjacent_square in all_bot_locations:
                return False
        return True

    def _destination(self, move: Move) -> Point:
        bot_location = self._game_state.get_bot_location(self._bot_id)
        step1_destination = move.step1.destination_from(bot_location,
                                   height=self._game_state.get_plan_height(),
                                   width=self._game_state.get_plan_width())
        if not move.step2:
            return step1_destination
        else:
            return move.step2.destination_from(step1_destination,
                                   height=self._game_state.get_plan_height(),
                                   width=self._game_state.get_plan_width())
