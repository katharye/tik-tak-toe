# domain/interfaces/bot_strategy_interface.py
from abc import ABC, abstractmethod
from domain.model import Game


class IBotStrategy(ABC):

    @abstractmethod
    def get_next_move(self, game: Game) -> tuple[int, int] | None:
        """Возвращает координаты следующего хода (row, col)."""
        pass