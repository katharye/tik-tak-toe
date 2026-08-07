# datasource/mapper/datasource_mapper.py

from uuid import UUID
from datasource.model import GameEntity
from domain import Game, Board

class DatasourceGameMapper:

    @classmethod
    def to_domain(cls, entity: GameEntity) -> Game:
            return Game(
                game_id=UUID(entity.game_id), 
                board=entity.board
            )

    @classmethod
    def to_data(cls, domain: Game) -> GameEntity:
        if isinstance(domain, Game):
            return GameEntity(
                game_id=str(domain.uuid),
                board=domain.board.values
            )