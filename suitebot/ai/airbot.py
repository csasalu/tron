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
STRAIGHT_DOUBLE_MOVES = tuple([Move(d, d) for d in ALL_DIRECTIONS])
SILLY_PAIRS = (
    (UP,DOWN),
    (DOWN,UP),
    (LEFT,RIGHT),
    (RIGHT,LEFT),
)
DETOUR_DOUBLE_MOVES = tuple([Move(d1, d2) for (d1, d2) in
                             itertools.product(ALL_DIRECTIONS, ALL_DIRECTIONS)
                             if d1 != d2 and (d1,d2) not in SILLY_PAIRS])

NOOK_PENALTY = -100
COLLISION_PENALTY = -200
CLOSE_TO_WALLS_REWARD = 30


class Airbot(BotAi):
    """OpenAir team's bot AI.  Based off SampleBot AI."""

    _bot_id = None  # type: int
    _game_state = None  # type: GameState

    def get_move_suppliers(self):
        return (
            {
                'func': self._safe_move_supplier,
                'coefficient': 1.0,
            },
            {
                'func': self._safe_haste_move_supplier,
                'coefficient': 1.2,
            },
            {
                'func': self._safe_detour_move_supplier,
                'coefficient': 0.8,
            },
        )

    def make_move(self, bot_id: int, game_state: GameState) -> Move:
        self._bot_id = bot_id
        self._game_state = game_state
        if self._is_dead():
            return DEFAULT_MOVE

        move_suppliers = self.get_move_suppliers()
        move_score_calculators = (
            self._nook_risk_calculator,
            self._collision_risk_calculator,
            self._staying_close_to_walls_calculator,
        )
        scored_moves = []
        for move_supplier in move_suppliers:
            supplier_func = move_supplier['func']
            supplier_coeff = move_supplier['coefficient']

            try:
                supplied_moves = list(supplier_func())
                if not supplied_moves:
                    continue
                for move in supplied_moves:
                    score = 1.0
                    for score_calculator in move_score_calculators:
                        score += score_calculator(move)
                    scored_moves.append(
                        {
                            'move': move,
                            'score': score * supplier_coeff,
                        }
                    )
            except StopIteration:
                continue
        if scored_moves:
            sorted_moves = list(sorted(scored_moves, key=lambda elem: elem['score']))
            best_move = sorted_moves[-1]['move']
            return best_move
        return DEFAULT_MOVE

    def get_name(self) -> str:
        return BOT_NAME

    def _is_dead(self) -> bool:
        return self._bot_id not in self._game_state.get_live_bot_ids()

    def _safe_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_safe_move, SINGLE_MOVES)

    def _safe_haste_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_safe_double_move, STRAIGHT_DOUBLE_MOVES)

    def _safe_detour_move_supplier(self) -> Iterator[Move]:
        return filter(self._is_safe_double_move, DETOUR_DOUBLE_MOVES)

    def _is_safe_move(self, move: Move) -> bool:
        dest = self._destination(move)
        return dest not in self._game_state.get_obstacle_locations()

    def _is_safe_double_move(self, move: Move) -> bool:
        dests = list(self._destinations(move))
        unpassable_points = self._game_state.get_obstacle_locations()
        return all(dest not in unpassable_points for dest in dests)

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

    def _staying_close_to_walls_calculator(self, move: Move) -> float:
        if self._is_move_close_to_walls(move):
            return CLOSE_TO_WALLS_REWARD
        else:
            return 0

    def _is_move_close_to_walls(self, move: Move) -> bool:
        dests = self._destinations(move)
        for dest in dests:
            walls_nearby_cnt = 0
            for adj_dir in ALL_DIRECTIONS:
                adj_cell = adj_dir.destination_from(dest,
                                  height=self._game_state.get_plan_height(),
                                  width=self._game_state.get_plan_width())
                if adj_cell in self._game_state.get_obstacle_locations():
                    walls_nearby_cnt += 1
            # 1-2 walls are fine, otherwise not as good
            if walls_nearby_cnt not in (1, 2):
                return False
        return True


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
        dests = self._destinations(move)
        for dest in dests:
            if not self._is_clear_from_enemies(dest):
                return False
        return True

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
        return list(self._destinations(move))[-1]

    def _destinations(self, move: Move) -> Point:
        bot_location = self._game_state.get_bot_location(self._bot_id)
        prev_loc = bot_location
        for step_name in ('step1', 'step2'):
            step = getattr(move, step_name)
            if not step:
                continue
            height = self._game_state.get_plan_height()
            width = self._game_state.get_plan_width()
            dest = step.destination_from(prev_loc,
                                         height=height,
                                         width=width)
            prev_loc = dest
            yield dest
