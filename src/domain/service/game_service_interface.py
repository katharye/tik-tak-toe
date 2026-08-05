from abc import ABC, abstractmethod
from domain.model import Game, Side

class GameServiceABC(ABC):

    @abstractmethod
    def get_next_move(self, game: Game) -> tuple[int, int]:
        """Возвращает координаты (row, col) следующего хода ИИ (Minimax)."""
        ...

    @abstractmethod
    def validate_field(self, old_game: Game | None, new_game: Game) -> bool:
        """Проверяет валидность ходов (что не переписаны прошлые ходы и сделан ровно 1 ход)."""
        ...

    @abstractmethod
    def check_game_finish(self, game: Game) -> tuple[bool, Side | None]:
        """Возвращает (is_over, winner), где winner: Player, Machine, Draw или None."""
        ...