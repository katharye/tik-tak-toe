# web/model/game_dto.py
from typing import Self, Optional
from dataclasses import dataclass

from web.model.board_dto import BoardDTO 

@dataclass
class GameDTO:
    game_id: str
    board: BoardDTO
    type: str
    state: str
    player_x_id: str
    player_o_id: str
    current_turn_id: str

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "board": self.board.to_dict(),
            "type": self.type,
            "state": self.state,
            "player_x_id": self.player_x_id,
            "player_o_id": self.player_o_id,
            "current_turn_id": self.current_turn_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        game_id = data.get("game_id", None)
        board = data.get("board", None)

        type = data.get("type", None)
        state = data.get("state", None)

        player_x_id = data.get("player_x_id", None)
        player_o_id = data.get("player_o_id", None)
        current_turn_id = data.get("current_turn_id", None)

        if None in (game_id, board, type, state, player_x_id, player_o_id, current_turn_id):
            return None

        board_dto = BoardDTO.from_dict(board)
        if board_dto is None:
            return None

        return GameDTO(
            game_id=game_id, 
            board=board_dto,
            type=type,
            state=state,
            player_x_id=player_x_id,
            player_o_id=player_o_id,
            current_turn_id=current_turn_id,
            )