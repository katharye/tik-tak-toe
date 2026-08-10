# datasource/repository/game_repository_impl.py
from sqlalchemy import select, or_, func, case, Float, cast, desc
from datasource.db import SessionLocal
from datasource.mapper import DatasourceGameMapper
from datasource.model import GameEntity, PlayerEntity
from domain import Game, IGameRepository, GameType, GameState, LiderBoardProfile

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
                GameEntity.type == GameType.VSPLAYER,
                GameEntity.state == GameState.WAITING)

            games_entity = session.scalars(games_select).all()

            return [DatasourceGameMapper.to_domain(game_entity) for game_entity in games_entity]

    def get_finished_by_user(self, user_id: str | UUID) -> list[Game]: 
        with SessionLocal() as session:
            games = select(GameEntity).where(
                GameEntity.state.in_([GameState.WIN_O, GameState.WIN_X, GameState.DRAW]),
                or_(str(user_id) == GameEntity.player_x_id,
                    str(user_id) == GameEntity.player_o_id
                )
            )

            games_entity = session.scalars(games).all()

            return [DatasourceGameMapper.to_domain(game_entity) for game_entity in games_entity]

    def get_leaderboard(self, limit: int) -> list[LiderBoardProfile]: 
        with SessionLocal() as session:
            wins_expr = case(
                (
                    or_(
                        (GameEntity.player_x_id == PlayerEntity.player_id) & (GameEntity.state == GameState.WIN_X),
                        (GameEntity.player_o_id == PlayerEntity.player_id) & (GameEntity.state == GameState.WIN_O),
                    ),
                    1
                ),
                else_=0
            )

            total_expr = case(
                (
                    GameEntity.state.in_([GameState.WIN_X, GameState.WIN_O, GameState.DRAW]), 1
                ), 
                else_=0
            )

            wins_sum = cast(func.sum(wins_expr), Float)
            total_sum = cast(func.sum(total_expr), Float)
            ratio_expr = wins_sum / func.nullif(total_sum, 0)
            
            query = (
                select(
                    PlayerEntity.player_id,
                    PlayerEntity.player_login,
                    ratio_expr.label("win_ratio")
                )
                .select_from(PlayerEntity)
                .join(
                    GameEntity,
                    or_(
                        PlayerEntity.player_id == GameEntity.player_x_id,
                        PlayerEntity.player_id == GameEntity.player_o_id,
                    )
                )
                .where(GameEntity.state.in_([GameState.WIN_X, GameState.WIN_O, GameState.DRAW]))
                .group_by(PlayerEntity.player_id, PlayerEntity.player_login)
                .order_by(desc(ratio_expr))
                .limit(limit)
            )

            result = session.execute(query).all()
            
            return [
                LiderBoardProfile(
                    player_id=UUID(row.player_id),
                    login=row.player_login,
                    win_ratio=float(row.win_ratio) if row.win_ratio is not None else 0.0
                )
                for row in result
            ]