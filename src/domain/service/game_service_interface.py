# domain/service/game_service_interface.py
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from domain.model import Game, Board, GameType

class IGameService(ABC):

    @abstractmethod
    def create_game(self, player_id: UUID, game_type: GameType) -> Game: ...
        
    @abstractmethod
    def join_game(self, game_id: UUID, player_id: UUID) -> Optional[Game]: ...
    
    @abstractmethod
    def get_available_games(self) -> list[Game]: ...
    
        
    @abstractmethod
    def make_move(self, game_id: UUID, player_id: UUID, row: int, col: int) -> Optional[Game]: ...
        
    @abstractmethod
    def get_game(self, game_id: UUID) -> Optional[Game]: ...


    @abstractmethod
    def get_next_move(self, game: Game) -> Game: ...

    @staticmethod
    @abstractmethod
    def check_game_finish(board: Board) -> tuple[bool, int | None]:
        """Возвращает (is_over, winner), где winner: Player(1), Machine(-1), Draw(0) или None."""
        ...