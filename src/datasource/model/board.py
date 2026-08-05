from dataclasses import dataclass

@dataclass
class BoardEntity:
    matrix: list[list[int]]

    def __post_init__(self):
        self.matrix = [row.copy() for row in self.matrix]
