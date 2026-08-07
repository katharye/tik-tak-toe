# web/model/game_dto.py
from typing import Self, Optional
from dataclasses import dataclass

from web.model.board_dto import BoardDTO 

@dataclass
class GameDTO:
    game_id: str
    board: BoardDTO

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "board": self.board.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        game_id = data.get("game_id", None)
        board = data.get("board", None)
        if game_id is None or board is None:
            return None

        board_dto = BoardDTO.from_dict(board)
        if board_dto is None:
            return None

        return GameDTO(game_id=game_id, board=board_dto)