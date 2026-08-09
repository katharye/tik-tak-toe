from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class CreateGameRequestDTO:
    type: str

    def to_dict(self) -> dict:
        return {
            "type": self.type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        type = data.get("type", None)
        if type is None:
            return None
        
        return CreateGameRequestDTO(type=type)    