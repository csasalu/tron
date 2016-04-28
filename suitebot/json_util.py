import json

from suitebot.game import game_state_factory
from suitebot.game.game_state import GameState


def game_state_from_json(move_request_json: str) -> GameState:
    move_request = json.loads(move_request_json)
    game_plan = game_state_factory.create_from_game_plan_lines(move_request['gamePlan'])
    # noinspection PyProtectedMember
    return GameState(
        plan_width=game_plan.get_plan_width(),
        plan_height=game_plan.get_plan_height(),
        bot_ids=move_request['botIds'],
        live_bot_ids=move_request['liveBotIds'],
        bot_location_map=game_plan._bot_location_map,
        obstacles=game_plan.get_obstacle_locations(),
    )


def your_bot_id_from_json(move_request_json: str) -> int:
    move_request = json.loads(move_request_json)
    return move_request['yourBotId']
