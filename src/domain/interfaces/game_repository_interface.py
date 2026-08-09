# domain/interfaces/game_repository_interface.py
from domain.model import Game

from abc import ABC, abstractmethod
from uuid import UUID

class IGameRepository(ABC):

    @abstractmethod
    def save(self, game: Game) -> None: ...

    @abstractmethod
    def get(self, game_id: str | UUID) -> Game | None: ...

    @abstractmethod
    def get_available(self) -> list[Game]: ...