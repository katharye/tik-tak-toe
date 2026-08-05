from domain.interfaces import IBotStrategy
from domain.model import Game, Board, Side

from domain.service.game_service_impl import GameService

from dataclasses import dataclass

@dataclass(frozen=True)
class MinimaxScores:
    """Веса исходов игры для алгоритма Minimax."""
    WIN: int = 10
    LOSS: int = -10
    DRAW: int = 0

class BotStrategy_MinMax(IBotStrategy):
    def _minimax(self, board: Board, depth: int, bot_turn: bool) -> int:
        win, winner = GameService.check_game_finish(board)
        if win:
            match winner:
                case Side.PLAYER:
                    return MinimaxScores.LOSS + depth
                case Side.MACHINE:
                    return MinimaxScores.WIN - depth
                case Side.CLEAR:
                    return MinimaxScores.DRAW

        best_score = float("-inf") if bot_turn else float("inf")

        for y in range(3):
            for x in range(3):
                if board[y][x] == Side.CLEAR:

                    board[y][x] = Side.MACHINE if bot_turn else Side.PLAYER
                    score = self._minimax(board, depth + 1, not(bot_turn))
                    board[y][x] = Side.CLEAR

                    comparator = max if bot_turn else min
                    best_score = comparator(best_score, score)

        return best_score
                    
        
            

    def get_next_move(self, game: Game) -> tuple[int, int] | None:
        move = None
        board = game.board.copy()
        best_score = float('-inf')
        for y in range(3):
            for x in range(3):
                if board[y][x] == Side.CLEAR:

                    board[y][x] = Side.MACHINE
                    score = self._minimax(board, 0, bot_turn=False)
                    board[y][x] = Side.CLEAR
                    if score > best_score:
                        best_score = score
                        move = (y, x)
        return move
