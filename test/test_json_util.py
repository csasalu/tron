import json

from suitebot import json_util
from suitebot.game.game_state import GameState
from suitebot.game.point import Point


def test_game_state_from_json():
    data = {
        'gamePlan': [
            '* 2',
            ' 1 ',
            ' **',
        ],
        'botIds': [1, 2, 3],
        'liveBotIds': [1, 2],
    }
    data_json = json.dumps(data)
    state = json_util.game_state_from_json(data_json)
    assert isinstance(state, GameState)
    assert state.get_plan_width() == 3
    assert state.get_plan_height() == 3
    assert state.get_all_bot_ids() == (1, 2, 3)
    assert state.get_live_bot_ids() == frozenset((1, 2))
    assert state.get_bot_location(1) == Point(1,1)
    assert state.get_bot_location(2) == Point(2,0)
    assert state.get_bot_location(3) == None

    obstacle_locations = state.get_obstacle_locations()
    assert len(obstacle_locations) == 3
    assert Point(0,0) in obstacle_locations
    assert Point(1,2) in obstacle_locations
    assert Point(2,2) in obstacle_locations


def test_bot_id_from_json():
    data = {
        'yourBotId': 'Albatross!',
    }
    data_json = json.dumps(data)
    rv = json_util.your_bot_id_from_json(data_json)
    assert rv == 'Albatross!'
