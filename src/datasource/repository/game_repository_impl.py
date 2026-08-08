# datasource/repository/game_repository_impl.py
from datasource.db import SessionLocal
from datasource.mapper import DatasourceGameMapper
from datasource.model import GameEntity
from domain import Game, IGameRepository

from uuid import UUID

class GameRepository(IGameRepository):
    def __init__(self): ...

    def save(self, game: Game) -> None:
        with SessionLocal() as session:
            existing = session.get(GameEntity, str(game.uuid))
            if existing:
                existing.board = game.board.values
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