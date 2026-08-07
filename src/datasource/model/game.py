from typing import List
from sqlalchemy import String, Integer, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from datasource.db.base import Base


class GameEntity(Base):
    __tablename__ = "games"

    game_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, primary_key=True)
    board: Mapped[List[List[int]]] = mapped_column(ARRAY(Integer, dimensions=2))
