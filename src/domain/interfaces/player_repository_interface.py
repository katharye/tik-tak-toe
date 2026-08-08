from domain.model import Player

from abc import ABC, abstractmethod
from uuid import UUID

class IPlayerRepository(ABC):

    @abstractmethod
    def save(self, player: Player) -> None: ...
    
    @abstractmethod
    def get(self, player_id: str | UUID) -> Player | None: ...

    @abstractmethod
    def get_by_login(self, login: str) -> Player | None: ...