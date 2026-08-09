from dataclasses import dataclass
from typing import Self, Optional

@dataclass
class MoveRequestDTO:
    row: int
    col: int

    def to_dict(self) -> dict:
        return {
            "row": self.row,
            "col": self.col,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        row = data.get("row", None)
        col = data.get("col", None)
        if None not in (row, col) and (0 <= row <= 2 and 0 <= col <= 2):
            return MoveRequestDTO(row=int(row), col=int(col))    

        return None
        
