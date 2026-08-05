from domain.service.game_service_interface import GameServiceABC
from domain.model import Game, Board, Side

from domain.interfaces import IGameRepository, IBotStrategy 

class GameService(GameServiceABC):
    def __init__(self, repository: IGameRepository, bot_strategy: IBotStrategy | None):
        super().__init__()
        self.repository = repository
        self.bot_strategy = bot_strategy

    @staticmethod
    def validate_field(new_game: Game, old_game: Game | None = None) -> bool:
        if old_game is None:
            player_steps = sum(row.count(Side.PLAYER) for row in new_game.board.values)
            return player_steps in (8, 9)

        steps = 0
        for i in range(3):
            for j in range(3):
                old_val = old_game.board[i][j]
                new_val = new_game.board[i][j]

                if old_val != new_val and old_val != Side.CLEAR:
                    return False

                if old_val != new_val:
                    steps += 1
                
        return steps == 1

    @staticmethod
    def check_game_finish(board: Board) -> tuple[bool, int | None]:
        lines = []

        for i in range(3):
            lines.append((board[i][0], board[i][1], board[i][2]))
            lines.append((board[0][i], board[1][i], board[2][i]))

        lines.append((board[0][0], board[1][1], board[2][2]))
        lines.append((board[0][2], board[1][1], board[2][0]))

        for line in lines:
            if abs(sum(line)) == 3 and Side.CLEAR not in line:
                winner = line[0]
                return (True, winner)

        has_empty_cells = any(Side.CLEAR in row for row in board.values)
        if not has_empty_cells:
            return (True, Side.CLEAR)

        return (False, None) 

    def get_next_move(self, game: Game) -> tuple[int, int] | None:
        if not self.bot_strategy:
            raise ValueError("Для этого режима игры не задана стратегия бота.")
        return self.bot_strategy.get_next_move(game=game)