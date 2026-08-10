from typing import List
from sqlalchemy import String, Integer, ARRAY, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datasource.db.base import Base


class GameEntity(Base):
    __tablename__ = "games"

    game_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, primary_key=True)
    board: Mapped[List[List[int]]] = mapped_column(ARRAY(Integer, dimensions=2))

    type:  Mapped[str] = mapped_column(String(10), index=True, nullable=True)
    state: Mapped[str] = mapped_column(String(10), index=True, nullable=True)
                
    player_x_id:        Mapped[str] = mapped_column(String(36), index=True, nullable=True)
    player_o_id:        Mapped[str] = mapped_column(String(36), index=True, nullable=True)
    current_turn_id: Mapped[str] = mapped_column(String(36), index=True, nullable=True)

    # created_at: Mapped[DateTime] = mapped_column(DateTime)