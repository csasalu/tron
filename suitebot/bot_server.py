import sys
from typing import List

#from suitebot.ai.sample_bot_ai import SampleBotAi
from suitebot.ai.airbot import Airbot
from suitebot.bot_request_handler import BotRequestHandler
from suitebot.server.simple_server import SimpleServer

DEFAULT_PORT = 9001


def _determine_port(args: List[str]) -> int:
    if len(args) == 1:
        return int(args[0])
    else:
        return DEFAULT_PORT


if __name__ == "__main__":
    #bot_ai = SampleBotAi() # replace with your own AI
    bot_ai = Airbot() # replace with your own AI

    port = _determine_port(sys.argv[1:])

    print("listening on port %i" % port)
    SimpleServer(port, BotRequestHandler(bot_ai)).run()
