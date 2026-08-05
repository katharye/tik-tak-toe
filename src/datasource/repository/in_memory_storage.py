from datasource.model import GameEntity

from threading import Lock

class InMemoryStorage:
    def __init__(self):
        self.data = {}
        self.lock = Lock()

    def add(self, game: GameEntity) -> None:
        with self.lock:
            game_copy = GameEntity(game_id=game.game_id, board=game.board)
            self.data[game.game_id] = game_copy

    def get(self, game_id: str) -> GameEntity | None:
        with self.lock:
            entity: GameEntity = self.data.get(game_id)
            if entity is None:
                return None

            return GameEntity(game_id=entity.game_id, board=entity.board)

    def delete(self, game_id: str) -> bool:
        with self.lock:
            return self.data.pop(game_id, None) is not None