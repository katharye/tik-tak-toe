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

        try:
            row_i = int(row)
            col_i = int(col)
        except (ValueError, TypeError):
            return None
        if 0 <= row_i <= 2 and 0 <= col_i <= 2:
            return MoveRequestDTO(row=row_i, col=col_i)

        return None
        
