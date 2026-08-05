from datasource.repository.game_repository_interface import IGameRepository
from datasource.repository.in_memory_storage import InMemoryStorage
from datasource.mapper import DatasourceMapper

from domain import Game

from uuid import UUID

class GameRepository(IGameRepository):
    def __init__(self, storage: InMemoryStorage | None = None):
        super().__init__()
        self.storage = storage if storage is not None else InMemoryStorage() 

    def save(self, game: Game) -> None:
        entity = DatasourceMapper.to_data(game)
        self.storage.add(entity)
        

    def get(self, game_id: str | UUID) -> Game | None:
        game_id = str(game_id)

        entity = self.storage.get(game_id)
        if entity is not None:
            return DatasourceMapper.to_domain(entity)

        return None