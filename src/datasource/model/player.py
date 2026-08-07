from sqlalchemy import String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from datasource.db.base import Base


class PlayerEntity(Base):
    __tablename__ = "player"

    player_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, primary_key=True)
    player_password: Mapped[str] = mapped_column(String(64), unique=False)