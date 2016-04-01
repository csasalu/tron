from abc import ABCMeta, abstractmethod
from typing import Optional

from suitebot.game.game_state import GameState
from suitebot.game.move import Move


class BotAi:
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_move(self, bot_id: int, game_state: GameState) -> Optional[Move]:
        """Returns the move that the AI intends to play.

        :param bot_id: ID of the bot operated by the AI
        :param game_state: current game state
        :return the move that the AI intends to play
        """

    @abstractmethod
    def get_name(self) -> str:
        """Returns the name of the bot.

        :return the name of the bot
        """
