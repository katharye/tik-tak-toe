from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class JWTResponseDTO:
    type: str
    access_token: Optional[str]
    refresh_token: Optional[str]

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }