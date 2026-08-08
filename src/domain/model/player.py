from uuid import UUID

class Player:
    def __init__(self, player_id: UUID, login: str, password: str):
        self.player_id = player_id
        self.login = login
        self.password = password