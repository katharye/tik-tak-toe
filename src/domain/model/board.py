from __future__ import annotations

class Board:
    def __init__(self, board_values: list[list[int]] | None = None):
        if board_values and len(board_values) == 3:
            validated_board = []
            for row in board_values:
                if len(row) == 3 and all(x in (-1, 0, 1) for x in row):
                    validated_board.append(row.copy())
                else :
                    break

            if len(validated_board) == 3:
                self.values = validated_board
                return
    
        self.values = [[-1, -1, -1] for _ in range(3)]

    def copy(self) -> Board:
        new = Board.__new__(Board)
        new.values = [row.copy() for row in self.values]
        return new

    def __getitem__(self, index: int) -> list[int]:
        """Позволяет обращаться к клеткам напрямую: board[0][1]"""
        return self.values[index]