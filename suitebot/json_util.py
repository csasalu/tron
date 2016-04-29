import json

from suitebot.game import game_state_factory
from suitebot.game.game_state import GameState
from suitebot.game.bot import Bot
from suitebot.game.point import Point


def game_state_from_json(move_request_json: str) -> GameState:
    move_request = json.loads(move_request_json)
    game_state = game_state_factory.create_from_game_plan_lines(move_request['gamePlan'])

    # update bots: set is_alive flag
    # (we aren't sure how a dead bot is represented on plan lines:
    # maybe it isn't there, maybe it's there)
    for id in move_request['botIds']:
        try:
            bot = game_state.get_bot(id)
        except KeyError:
            bot = Bot(id=id, name=id)
            game_state._bots[id] = bot
        bot.is_alive = id in move_request['liveBotIds']

    # update bots: set segments
    # (N/A for this API: we don't track bots' tails)

    return game_state


def your_bot_id_from_json(move_request_json: str) -> int:
    move_request = json.loads(move_request_json)
    return move_request['yourBotId']


def your_bot_id_from_tron_league_json(move_request_json: str) -> int:
    move_request = json.loads(move_request_json)
    return move_request['aiPlayerId']


def game_state_from_tron_league_json(move_request_json: str) -> (int, GameState):
    move_request = json.loads(move_request_json)
    meta = move_request['gameState']

    game_state_data = move_request['gameState']
    game_plan_data = game_state_data['gamePlan']

    # TODO:
    # use gamePlan.startingPositions
    # use gamePlan.walls

    bots = {}

    # add bots
    for item in game_state_data['players']:
        id = int(item['id'])
        bots[id] = Bot(**item)

    # update bots: set is_alive flag
    for item in game_state_data['livePlayers']:
        id = int(item['id'])
        bot = bots[id]
        #assert item['name'] == bot.name
        bot.is_alive = True

    # update bots: set segments
    for id, item in game_state_data['playerStateMap'].items():
        id = int(id)
        bot = bots[id]
        segments = item['segments']
        for point_data in segments:
            point = Point(**point_data)
            bot.add_segment(point)

    return GameState(
        plan_width=game_plan_data['width'],
        plan_height=game_plan_data['height'],
        bots=bots,
    )
