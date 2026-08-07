# domain/service/game_service_impl.py
from domain.service.game_service_interface import GameServiceABC
from domain.model import Game, Board, Side

from domain.interfaces import IGameRepository, IBotStrategy 

class GameService(GameServiceABC):
    def __init__(self, repository: IGameRepository, bot_strategy: IBotStrategy | None = None):
        self.repository = repository
        self.bot_strategy = bot_strategy

    def validate_field(self, game: Game) -> bool:
        old_game = self.repository.get(game_id=game.uuid) 
        if old_game is None:
            player_steps = sum(row.count(Side.PLAYER) for row in game.board.values)
            machine_steps = sum(row.count(Side.MACHINE) for row in game.board.values)
            # Новая игра: либо пустое поле, либо один ход игрока
            return machine_steps == 0 and player_steps in (0, 1)

        steps = 0
        for i in range(3):
            for j in range(3):
                old_val = old_game.board[i][j]
                new_val = game.board[i][j]

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

    def get_next_move(self, game: Game) -> Game:
        if not self.bot_strategy:
            raise ValueError("Для этого режима игры не задана стратегия бота.")
        next_step = self.bot_strategy.get_next_move(game=game)
        if next_step is None:
            return game
        row, col = next_step
        next_step_game = game.copy()
        next_step_game.board[row][col] = Side.MACHINE

        self.repository.save(next_step_game)
        return next_step_game