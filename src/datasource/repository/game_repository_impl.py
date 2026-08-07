# datasource/repository/game_repository_impl.py
from datasource.repository.in_memory_storage import InMemoryStorage
from datasource.mapper import DatasourceMapper

from domain import Game, IGameRepository

from uuid import UUID

class GameRepository(IGameRepository):
    def __init__(self, storage: InMemoryStorage):
        super().__init__()
        self.storage = storage 

    def save(self, game: Game) -> None:
        entity = DatasourceMapper.to_data(game)
        self.storage.add(entity)
        

    def get(self, game_id: str | UUID) -> Game | None:
        game_id = str(game_id)

        entity = self.storage.get(game_id)
        if entity is not None:
            return DatasourceMapper.to_domain(entity)

        return None