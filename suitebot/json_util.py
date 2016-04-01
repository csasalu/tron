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
        bot_location_map=game_plan._bot_location_map,
        bot_energy_map=move_request['botEnergyMap'],
        live_bot_ids=game_plan.get_live_bot_ids(),
        obstacles=game_plan.get_obstacle_locations(),
        treasures=game_plan.get_treasure_locations(),
        batteries=game_plan.get_battery_locations()
    )


def your_bot_id_from_json(move_request_json: str) -> int:
    move_request = json.loads(move_request_json)
    return move_request['yourBotId']