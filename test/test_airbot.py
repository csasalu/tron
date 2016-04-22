from suitebot.ai.airbot import Airbot
from suitebot.game import game_state_factory
from suitebot.game.direction import *
from suitebot.game.move import Move


class BaseAirbotTest:

    ME = 1    # default bot ID

    def go(self, game_plan):
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        bot = Airbot()
        return bot.make_move(self.ME, game_state)


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


class TestAirbotTreasure(BaseAirbotTest):

    def test_should_collect_nearest_treasure(self):
        game_plan = [
            '****',
            '*1 !',
            '*!  ',
        ]
        assert self.go(game_plan).step1 == DOWN

    def test_should_collect_treasure_with_double_move(self):
        game_plan = [
            '****',
            '*1 !',
            '*   ',
        ]
        assert self.go(game_plan) == Move(RIGHT, RIGHT)


class TestAirbotBattery(BaseAirbotTest):

    def test_should_prefer_treasure_to_battery_if_distance_is_equal(self):
        game_plan = [
            '****',
            '*1 !',
            '* + ',
        ]
        assert self.go(game_plan) == Move(RIGHT, RIGHT)

    def test_should_prefer_battery_to_treasure_if_closer(self):
        game_plan = [
            '****',
            '*1 !',
            '*+  ',
        ]
        assert self.go(game_plan).step1 == DOWN
