# domain/model/game.py
from __future__ import annotations
from uuid import uuid4, UUID

from domain.model.board import Board

class Game:
    def __init__(self, game_id: UUID | None = None, board: Board | None = None):
        if game_id is None:
            self.uuid = uuid4()
        else:
            self.uuid = game_id
        if board:
            self.board = board.copy()
        else:
            self.board = Board()

    def copy(self) -> Game:
        new = Game.__new__(Game)
        new.uuid = self.uuid
        new.board = self.board.copy()
        return new