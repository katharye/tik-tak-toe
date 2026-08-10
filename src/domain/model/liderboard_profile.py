from dataclasses import dataclass
from uuid import UUID

@dataclass
class LiderBoardProfile:
    player_id: UUID
    login: str
    win_ratio: float