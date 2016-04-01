from suitebot import json_util
from suitebot.ai.bot_ai import BotAi
from suitebot.server.simple_request_handler import SimpleRequestHandler

NAME_REQUEST = "NAME"


class BotRequestHandler(SimpleRequestHandler):
    def __init__(self, bot_ai: BotAi) -> None:
        self._bot_ai = bot_ai

    def process_request(self, request: str) -> str:
        try:
            return self._process_request_internal(request)
        except Exception as e:
            print(e)
            return str(e)

    def _process_request_internal(self, request: str) -> str:
        if request == NAME_REQUEST:
            return self._bot_ai.get_name()
        return self._process_move_request(request)

    def _process_move_request(self, request: str) -> str:
        bot_id = json_util.your_bot_id_from_json(request)
        game_state = json_util.game_state_from_json(request)
        return str(self._bot_ai.make_move(bot_id, game_state))
