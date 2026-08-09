# datasource/repository/game_repository_impl.py
from sqlalchemy import select
from datasource.db import SessionLocal
from datasource.mapper import DatasourceGameMapper
from datasource.model import GameEntity
from domain import Game, IGameRepository, GameType, GameState

from uuid import UUID

class GameRepository(IGameRepository):
    def __init__(self): ...

    def save(self, game: Game) -> None:
        with SessionLocal() as session:
            existing = session.get(GameEntity, str(game.uuid))
            if existing:
                existing.board = game.board.values
                existing.type = game.type if game.type is not None else None
                existing.state = game.state if game.state is not None else None
                existing.current_turn_id = str(game.current_turn_id) if game.current_turn_id is not None else None
                existing.player_x_id = str(game.player_x_id) if game.player_x_id is not None else None
                existing.player_o_id = str(game.player_o_id) if game.player_o_id is not None else None
            else:
                entity = DatasourceGameMapper.to_data(game)
                session.add(entity)
            session.commit()
        

    def get(self, game_id: str | UUID) -> Game | None:
        with SessionLocal() as session:
            entity = session.get(GameEntity, str(game_id))
            if entity is not None:
                return DatasourceGameMapper.to_domain(entity)
            return None

    def get_available(self) -> list[Game]: 
        with SessionLocal() as session:
            games_select = select(GameEntity).where(
                GameEntity.type ==GameType.VSPLAYER,
                GameEntity.state == GameState.WAITING)

            games_entity = session.scalars(games_select).all()

            return [DatasourceGameMapper.to_domain(game_entity) for game_entity in games_entity]