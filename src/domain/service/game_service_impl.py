# domain/service/game_service_impl.py
from typing import Optional
from uuid import UUID

from domain.service.game_service_interface import IGameService
from domain.model import Game, Board, Side, GameType, GameState, LiderBoardProfile

from domain.interfaces import IGameRepository, IBotStrategy 

class GameService(IGameService):
    def __init__(self, repository: IGameRepository, bot_strategy: IBotStrategy):
        self.repository = repository
        self.bot_strategy = bot_strategy


    def create_game(self, player_id: UUID, game_type: GameType) -> Game: 
        game = Game(
            type=game_type,
            state= GameState.WAITING if game_type == GameType.VSPLAYER else GameState.TURN_X,
            player_x_id=player_id,
            current_turn_id=player_id
        )
        self.repository.save(game)
        return game
        
    def join_game(self, game_id: UUID, player_id: UUID) -> Optional[Game]: 
        game = self.repository.get(game_id)
        if game is None:
            return None

        if game.state != GameState.WAITING or game.type != GameType.VSPLAYER:
            return None

        if player_id == game.player_x_id:
            return None

        game.player_o_id = player_id
        game.state = GameState.TURN_X

        self.repository.save(game)

        return game

    def get_available_games(self) -> list[Game]: 
        return self.repository.get_available()
       
    def make_move(self, game_id: UUID, player_id: UUID, row: int, col: int) -> Optional[Game]: 
        game = self.get_game(game_id)
        if game is None or player_id != game.current_turn_id:
            return None

        if player_id != game.player_o_id and player_id != game.player_x_id:
            return None

        side = Side.X if player_id == game.player_x_id else Side.O

        if game.board[row][col] != Side.CLEAR:
            return None
        
        game.board[row][col] = side

        is_over, winner = self.check_game_finish(game.board)
        if is_over:
            match winner:
                case Side.X:
                    game.state=GameState.WIN_X
                case Side.O:
                    game.state=GameState.WIN_O
                case Side.CLEAR:
                    game.state=GameState.DRAW

            self.repository.save(game)
            return game

        if game.type == GameType.VSBOT:
            game.state = GameState.TURN_O
            game = self.get_next_move(game)
            
            is_over, winner = self.check_game_finish(game.board)
            if is_over:
                match winner:
                    case Side.X:
                        game.state=GameState.WIN_X
                    case Side.O:
                        game.state=GameState.WIN_O
                    case Side.CLEAR:
                        game.state=GameState.DRAW

                self.repository.save(game)
                return game  

            game.current_turn_id = game.player_x_id
            game.state = GameState.TURN_X


        elif game.type == GameType.VSPLAYER:
            game.current_turn_id = game.player_x_id if game.player_o_id == game.current_turn_id else game.player_o_id
            game.state = GameState.TURN_X if game.state == GameState.TURN_O else GameState.TURN_O

        self.repository.save(game)
        return game  
        
    def get_game(self, game_id: UUID) -> Optional[Game]:
        return self.repository.get(game_id)

    def get_leaderboard(self, limit: int) -> list[LiderBoardProfile]: 
        return self.repository.get_leaderboard(limit)


    def get_finished_games(self, player_id: UUID) -> list[Game]: 
        return self.repository.get_finished_by_user(player_id)

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
        next_step_game.board[row][col] = Side.O

        return next_step_game