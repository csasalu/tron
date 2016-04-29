import json

from suitebot import json_util
from suitebot.game.game_state import GameState
from suitebot.game.point import Point


def test_bot_id_from_json():
    data = {
        'yourBotId': 'Albatross!',
    }
    data_json = json.dumps(data)
    rv = json_util.your_bot_id_from_json(data_json)
    assert rv == 'Albatross!'


def test_game_state_from_suitebot_disccon2016_json():
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

    assert state.get_all_bot_ids() == frozenset({1, 2, 3})

    assert state.get_live_bot_ids() == frozenset({1, 2})

    assert state.get_bot_location(1) == Point(1,1)
    assert state.get_bot_location(2) == Point(2,0)
    assert state.get_bot_location(3) == None

    obstacle_locations = state.get_obstacle_locations()
    assert len(obstacle_locations) == 5    # bot heads counted, too
    assert Point(0,0) in obstacle_locations
    assert Point(1,2) in obstacle_locations
    assert Point(2,2) in obstacle_locations


TRON_LEAGUE_JSON = {
   'aiPlayerId': 1,
   'gameState': {
      'gamePlan': {
         'width': 30,
         'height': 30,
         'startingPositions': [
            { 'x': 5, 'y': 5 },
            { 'x': 15, 'y': 5 },
         ],
         'walls': [
            { 'x': 0, 'y': 0 },
         ],
      },
      'players': [
         {
            'id': 1,
            'name': 'Foo Bot',
         },
         {
            'id': 2,
            'name': 'Bar Bot',
         },
      ],
      'playerStateMap': {
         '1': {
            'segments': [
               { 'x': 5, 'y': 5 },
               { 'x': 4, 'y': 5 },
               { 'x': 3, 'y': 5 },
               { 'x': 2, 'y': 5 },
            ],
         },
         '2': {
            'segments': [
               { 'x': 15, 'y': 5 },
               { 'x': 16, 'y': 5 },
               { 'x': 17, 'y': 5 },
               { 'x': 18, 'y': 5 },
            ],
         },
      },
      'livePlayers': [
         {
            'id': 1,
            'name': 'Foo Bot',
         },
         {
            'id': 2,
            'name': 'Bar Bot',
         },
      ],
   },
}


def test_bot_id_from_tron_league_json():
    data = TRON_LEAGUE_JSON
    data_json = json.dumps(data)

    bot_id = json_util.your_bot_id_from_tron_league_json(data_json)

    assert bot_id == 1


def test_game_state_from_tron_league_json():
    data = TRON_LEAGUE_JSON
    data_json = json.dumps(data)

    state = json_util.game_state_from_tron_league_json(data_json)

    assert isinstance(state, GameState)

    assert state.get_plan_width()  == 30
    assert state.get_plan_height() == 30

    assert state.get_all_bot_ids() == frozenset((1, 2))

    # TODO: try adding a dead one
    assert state.get_live_bot_ids() == frozenset((1, 2))

    assert state.get_bot_location(1) == Point(2,5)
    assert state.get_bot_location(2) == Point(18,5)
    assert state.get_bot_location(3) == None

    obstacle_locations = state.get_obstacle_locations()
    assert len(obstacle_locations) == 8
    segments_of_bot_1 = {
        Point(5,5),
        Point(4,5),
        Point(3,5),
        Point(2,5),
    }
    segments_of_bot_2 = {
        Point(15,5),
        Point(16,5),
        Point(17,5),
        Point(18,5),
    }
    all_bot_segments = segments_of_bot_1 | segments_of_bot_2
    assert all_bot_segments == obstacle_locations
