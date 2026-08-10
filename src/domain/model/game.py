# domain/model/game.py
from uuid import uuid4, UUID
from typing import Optional, Self
from datetime import datetime

from domain.model.board import Board

class Game:
    def __init__(self, 
                 type: str,
                 state: str,
                
                 player_x_id: Optional[UUID] = None,
                 player_o_id: Optional[UUID] = None,

                 current_turn_id: Optional[UUID] = None,

                 game_id: Optional[UUID] = None, 
                 board: Optional[Board] = None,
                 created_at: Optional[datetime] = None
                 ):
        
        if game_id is None: 
            self.uuid = uuid4()
        else:
            self.uuid = game_id

        if board:
            self.board = board.copy()
        else:
            self.board = Board()

        self.player_o_id = player_o_id
        self.player_x_id = player_x_id

        self.current_turn_id = current_turn_id

        self.type = type
        self.state = state
        self.created_at = created_at
        
    def copy(self) -> Self:
        new = Game.__new__(Game)
        new.uuid = self.uuid
        new.board = self.board.copy()
        new.type = self.type
        new.state = self.state
        new.player_o_id = self.player_o_id
        new.player_x_id = self.player_x_id
        new.current_turn_id = self.current_turn_id
        new.created_at = self.created_at
        return new