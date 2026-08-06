from typing import Self, Optional
from dataclasses import dataclass

@dataclass
class BoardDTO:
    matrix: list[list[int]]

    def to_dict(self) -> dict:
        return {"matrix": [row.copy() for row in self.matrix]}

    @classmethod
    def from_dict(cls, data: dict) -> Optional[Self]:
        matrix = data.get("matrix")
        if matrix is None:
            return None
        
        return BoardDTO(matrix=[row.copy() for row in matrix])
    