from dataclasses import dataclass

from datasource.model.board import BoardEntity

@dataclass
class GameEntity:

    game_id: str
    board: BoardEntity

    def __post_init__(self):
        self.board = BoardEntity(self.board.matrix)

