# domain/model/game.py
from uuid import uuid4, UUID
from typing import Optional, Self

from domain.model.game_state import GameState
from domain.model.game_type import GameType
from domain.model.board import Board

class Game:
    def __init__(self, 
                 type: GameType,
                 state: GameState,
                
                 player_X: Optional[UUID] = None,
                 player_O: Optional[UUID] = None,

                 current_turn_id: Optional[UUID] = None,

                 game_id: Optional[UUID] = None, 
                 board: Optional[Board] = None,
                 ):
        
        if game_id is None: 
            self.uuid = uuid4()
        else:
            self.uuid = game_id

        if board:
            self.board = board.copy()
        else:
            self.board = Board()

        self.player_o_id = player_O
        self.player_x_id = player_X

        self.current_turn_id = current_turn_id

        self.type = type
        self.state = state
        
    def copy(self) -> Self:
        new = Game.__new__(Game)
        new.uuid = self.uuid
        new.board = self.board.copy()
        new.type = self.type
        new.state = self.state
        new.player_o_id = self.player_o_id
        new.player_x_id = self.player_x_id
        return new