from dataclasses import dataclass

@dataclass
class LiderBoardProfileDTO:
    player_id: str
    login: str
    win_ratio: float

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "login": self.login,
            "win_ratio": self.win_ratio,
        }