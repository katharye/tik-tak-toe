# web/mapper/dto_mapper.py
from domain import Game, Board
from web.model import GameDTO, BoardDTO

from typing import overload
from uuid import UUID

class WebGameMapper:

    @overload
    @classmethod
    def to_web(cls, domain: Game) -> GameDTO: ...

    @overload
    @classmethod
    def to_web(cls, domain: Board) -> BoardDTO: ...

    @overload
    @classmethod
    def to_domain(cls, web: GameDTO) -> Game: ...

    @overload
    @classmethod
    def to_domain(cls, web:BoardDTO) ->Board: ...

    @classmethod
    def to_web(cls, domain: Game | Board) -> GameDTO | BoardDTO:
        if isinstance(domain, Game):
            return GameDTO(
                game_id=str(domain.uuid),
                board=cls.to_web(domain.board),
                type=domain.type,
                state=domain.state,
                player_x_id=str(domain.player_x_id),
                player_o_id=str(domain.player_o_id),
                current_turn_id=str(domain.current_turn_id)
            )
        if isinstance(domain, Board):
            return BoardDTO(
                matrix=[row.copy() for row in domain.values]
            )

        raise TypeError(f"Unsupported entity type for to_web: {type(domain)}")

    @classmethod
    def to_domain(cls, web: GameDTO | BoardDTO) -> Game | Board:
        if isinstance(web, GameDTO):
            return Game(
                game_id=UUID(web.game_id),
                board=cls.to_domain(web.board),
                type=web.type,
                state=web.state,
                player_x_id=UUID(web.player_x_id),
                player_o_id=UUID(web.player_o_id),
                current_turn_id=UUID(web.current_turn_id)
            )   
        if isinstance(web, BoardDTO):
            return Board(
                [row.copy() for row in web.matrix]
            )

        raise TypeError(f"Unsupported entity type for to_domain: {type(web)}")
