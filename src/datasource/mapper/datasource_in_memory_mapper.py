# datasource/mapper/datasource_mapper.py

from uuid import UUID
from datasource.model import GameEntity, BoardEntity
from domain import Game, Board

class DatasourceInMemoryMapper:

    @classmethod
    def to_domain(cls, entity: GameEntity | BoardEntity) -> Game | Board:
        if isinstance(entity, GameEntity):
            return Game(
                game_id=UUID(entity.game_id), 
                board=cls.to_domain(entity.board)
            )

        if isinstance(entity, BoardEntity):
            return Board(entity.matrix)

        raise TypeError(f"Unsupported entity type for to_domain: {type(entity)}")

    @classmethod
    def to_data(cls, domain: Game | Board) -> GameEntity | BoardEntity:
        if isinstance(domain, Game):
            return GameEntity(
                game_id=str(domain.uuid),
                board=cls.to_data(domain.board)
            )
        
        if isinstance(domain, Board):            
            return BoardEntity(domain.values)

        raise TypeError(f"Unsupported entity type for to_data: {type(domain)}")
