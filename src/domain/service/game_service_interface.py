from abc import ABC, abstractmethod
from domain.model import Game, Board

class GameServiceABC(ABC):

    @abstractmethod
    def get_next_move(self, game: Game) -> tuple[int, int]:
        """Возвращает координаты (row, col) следующего хода ИИ (Minimax)."""
        ...

    @staticmethod
    @abstractmethod
    def validate_field(new_game: Game, old_game: Game | None = None) -> bool:
        """Проверяет валидность ходов (что не переписаны прошлые ходы и сделан ровно 1 ход)."""
        ...

    @staticmethod
    @abstractmethod
    def check_game_finish(board: Board) -> tuple[bool, int | None]:
        """Возвращает (is_over, winner), где winner: Player(1), Machine(-1), Draw(0) или None."""
        ...