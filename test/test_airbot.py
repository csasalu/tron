from suitebot.ai.airbot import Airbot
from suitebot.game import game_state_factory
from suitebot.game.direction import *
from suitebot.game.move import Move


# XXX actual threshold depends on concrete game rules
LOW_BOT_ENERGY = 1


class BaseAirbotTest:

    BOT_ID = 1    # default bot ID

    def go(self, game_plan, energy=None):
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        if energy:
            game_state._bot_energy_map = {
                self.BOT_ID: energy,
            }
        bot = Airbot()
        return bot.make_move(self.BOT_ID, game_state)


class TestTransparentBoundaries(BaseAirbotTest):
    """
    If we are a the rightmost square, we should see the free space
    on the corresponding leftmost one.
    """
    def test_should_see_the_other_side__up(self):
        game_plan = [
            '*1*',
            '***',
            '* *',
        ]
        assert self.go(game_plan) == Move(UP)

    def test_should_see_the_other_side__right(self):
        game_plan = [
            '***',
            ' *1',
            '***',
        ]
        assert self.go(game_plan) == Move(RIGHT)

    def test_should_see_the_other_side__down(self):
        game_plan = [
            '* *',
            '***',
            '*1*',
        ]
        assert self.go(game_plan) == Move(DOWN)

    def test_should_see_the_other_side__left(self):
        game_plan = [
            '***',
            '1* ',
            '***',
        ]
        assert self.go(game_plan) == Move(LEFT)

'''
class TestAirbotBoundaries(BaseAirbotTest):

    def test_should_avoid_top_boundary(self):
        game_plan = [
            ' 1 ',
            '   ',
            '   ',
        ]
        assert self.go(game_plan) != Move(UP)

    def test_should_avoid_right_boundary(self):
        game_plan = [
            '   ',
            '  1',
            '   ',
        ]
        assert self.go(game_plan) != Move(RIGHT)

    def test_should_avoid_bottom_boundary(self):
        game_plan = [
            '   ',
            '   ',
            ' 1 ',
        ]
        assert self.go(game_plan) != Move(DOWN)

    def test_should_avoid_left_boundary(self):
        game_plan = [
            '   ',
            '1  ',
            '   ',
        ]
        assert self.go(game_plan) != Move(LEFT)

    def test_should_leave_left_top_corner(self):
        game_plan = [
            '1  ',
            '   ',
            '   ',
        ]
        wrong_moves = Move(UP), Move(LEFT)
        assert self.go(game_plan) not in wrong_moves

    def test_should_leave_right_top_corner(self):
        game_plan = [
            '  1',
            '   ',
            '   ',
        ]
        wrong_moves = Move(UP), Move(RIGHT)
        assert self.go(game_plan) not in wrong_moves

    def test_should_leave_right_bottom_corner(self):
        game_plan = [
            '   ',
            '   ',
            '  1',
        ]
        wrong_moves = Move(DOWN), Move(RIGHT)
        assert self.go(game_plan) not in wrong_moves

    def test_should_leave_left_bottom_corner(self):
        game_plan = [
            '   ',
            '   ',
            '1  ',
        ]
        wrong_moves = Move(DOWN), Move(LEFT)
        assert self.go(game_plan) not in wrong_moves
'''

class TestAirbotObstacles(BaseAirbotTest):

    def test_should_avoid_obstacles(self):
        game_plan = [
            ' **',
            ' 1*',
            ' **',
        ]
        wrong_steps = UP, RIGHT, DOWN
        assert self.go(game_plan).step1 not in wrong_steps

    def test_should_avoid_obstacles_inversed(self):
        game_plan = [
            '** ',
            '*1 ',
            '** ',
        ]
        wrong_steps = UP, DOWN, LEFT
        assert self.go(game_plan).step1 not in wrong_steps

    def test_should_avoid_nooks__up(self):
        game_plan = [
            '***',
            '* *',
            ' 1 ',
        ]
        assert self.go(game_plan).step1 != UP

    def test_should_avoid_nooks__right(self):
        game_plan = [
            ' **',
            '1 *',
            ' **',
        ]
        assert self.go(game_plan).step1 != RIGHT

    def test_should_avoid_nooks__down(self):
        game_plan = [
            ' 1 ',
            '* *',
            '***',
        ]
        assert self.go(game_plan).step1 != DOWN

    def test_should_avoid_nooks__left(self):
        game_plan = [
            '** ',
            '* 1',
            '** ',
        ]
        assert self.go(game_plan).step1 != LEFT


class TestDistance:
    def test_distance_same_point(self):
        assert distance(Point(0, 0), Point(0, 0)) == 0

    def test_distance_adjacent_x(self):
        assert distance(Point(0, 0), Point(1, 0)) == 1

    def test_distance_adjacent_x_reversed(self):
        assert distance(Point(1, 0), Point(0, 0)) == 1

    def test_distance_adjacent_y(self):
        assert distance(Point(0, 0), Point(0, 1)) == 1

    def test_distance_adjacent_y_reversed(self):
        assert distance(Point(0, 1), Point(0, 0)) == 1

    def test_distance_diagonal_2steps(self):
        assert distance(Point(0, 0), Point(1, 1)) == 2

    def test_distance_diagonal_2steps_reversed(self):
        assert distance(Point(1, 1), Point(0, 0)) == 2

def distance(a, b):
    if a == b:
        return 0
    delta_x = abs(a.x - b.x)
    delta_y = abs(a.y - b.y)
    return delta_x + delta_y


