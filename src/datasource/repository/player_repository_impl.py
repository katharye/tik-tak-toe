# datasource/repository/game_repository_impl.py
from datasource.db import SessionLocal
from datasource.mapper import DatasourcePlayerMapper
from datasource.model import PlayerEntity
from domain import Player, IPlayerRepository

from uuid import UUID
from sqlalchemy import select

class PlayerRepository(IPlayerRepository):
    def __init__(self): ...

    def save(self, player: Player) -> None: 
        with SessionLocal() as session:
            entity = DatasourcePlayerMapper.to_data(player)
            existing = session.get(PlayerEntity, str(player.player_id))
            if existing:
                existing = entity
            else:
                session.add(entity)
            session.commit()

    def get(self, player_id: str | UUID) -> Player | None: 
        with SessionLocal() as session:
            entity = session.get(PlayerEntity, str(player_id))
            if entity is not None:
                return DatasourcePlayerMapper.to_domain(entity)
            return None

    def get_by_login(self, login: str) -> Player | None: 
        with SessionLocal() as session:
            result = session.execute(
                select(PlayerEntity).where(PlayerEntity.player_login == login)
            )
            entity = result.scalar_one_or_none()
            if entity:
                return DatasourcePlayerMapper.to_domain(entity)
        return None
            
