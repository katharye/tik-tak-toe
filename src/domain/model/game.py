from __future__ import annotations
from uuid import uuid4

from domain.model.board import Board

class Game:
    def __init__(self, board: Board | None = None):
        self.uuid = uuid4()
        if board:
            self.board = board.copy()
        else:
            self.board = Board()

    def copy(self) -> Game:
        new = Game.__new__(Game)
        new.uuid = self.uuid
        new.board = self.board.copy()
        return new