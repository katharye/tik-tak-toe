# datasource/mapper/datasource_mapper.py

from uuid import UUID
from datasource.model import GameEntity
from domain import Game, Board

class DatasourceGameMapper:

    @classmethod
    def to_domain(cls, entity: GameEntity) -> Game:
            return Game(
                game_id=UUID(entity.game_id), 
                board=Board(entity.board),
                type=entity.type,
                state=entity.state,
                player_x_id=UUID(entity.player_x_id) if entity.player_x_id is not None else None,
                player_o_id=UUID(entity.player_o_id) if entity.player_o_id is not None else None,
                current_turn_id=UUID(entity.current_turn_id) if entity.current_turn_id is not None else None
            )

    @classmethod
    def to_data(cls, domain: Game) -> GameEntity:
        if isinstance(domain, Game):
            return GameEntity(
                game_id=str(domain.uuid),
                board=domain.board.values,
                type=domain.type,
                state=domain.state,
                player_x_id=str(domain.player_x_id) if domain.player_x_id is not None else None,
                player_o_id=str(domain.player_o_id) if domain.player_o_id is not None else None,
                current_turn_id=str(domain.current_turn_id) if domain.current_turn_id is not None else None
            )