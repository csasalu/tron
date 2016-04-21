from suitebot.ai.airbot import Airbot
from suitebot.game import game_state_factory
from suitebot.game.direction import *
from suitebot.game.move import Move


class TestAirbotBasics:

    def test_should_avoid_obstacles(self):
        game_plan = [
            " **",
            " 1*",
            " **",
        ]
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        assert Airbot().make_move(1, game_state).step1 == LEFT

    def test_should_collect_nearest_treasure(self):
        game_plan = [
            "****",
            "*1 !",
            "*!  ",
        ]
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        assert Airbot().make_move(1, game_state).step1 == DOWN

    def test_should_collect_treasure_with_double_move(self):
        game_plan = [
            "****",
            "*1 !",
            "*   ",
        ]
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        assert Airbot().make_move(1, game_state) == Move(RIGHT, RIGHT)

    def test_should_prefer_treasure_to_battery_if_distance_is_equal(self):
        game_plan = [
            "****",
            "*1 !",
            "* + ",
        ]
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        assert Airbot().make_move(1, game_state) == Move(RIGHT, RIGHT)

    def test_should_prefer_battery_to_treasure_if_closer(self):
        game_plan = [
            "****",
            "*1 !",
            "*+  ",
        ]
        game_state = game_state_factory.create_from_game_plan_lines(game_plan)
        assert Airbot().make_move(1, game_state).step1 == DOWN
