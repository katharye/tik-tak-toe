from domain import Game, Board
from web.model import GameDTO, BoardDTO

from typing import overload
from uuid import UUID

class WebMapper:

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
                board=cls.to_web(domain.board)
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
                UUID(web.game_id),
                cls.to_domain(web.board)
            )   
        if isinstance(web, BoardDTO):
            return Board(
                [row.copy() for row in web.matrix]
            )

        raise TypeError(f"Unsupported entity type for to_domain: {type(web)}")
