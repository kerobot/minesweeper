from dataclasses import dataclass
from typing import List, Callable, Optional, Set, Tuple
import random
from .board_core import Board, Cell


class MinesweeperGame:
    def __init__(
        self,
        rows: int,
        cols: int,
        mine_count: int,
        *,
        rng: Optional[random.Random] = None,
        preset_mines: Optional[Set[Tuple[int, int]]] = None,
    ):
        self.board = Board(rows, cols, mine_count, rng=rng, preset_mines=preset_mines)

    def reset(self) -> None:
        self.board.reset()

    def reveal(self, r: int, c: int) -> None:
        cell = self.board.get_cell(r, c)
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.adjacent == 0 and not cell.is_mine:
            self.board.for_each_neighbor(r, c, lambda nr, nc: self.reveal(nr, nc))

    def toggle_flag(self, r: int, c: int) -> bool:
        cell = self.board.get_cell(r, c)
        if cell.is_revealed:
            return False
        cell.is_flagged = not cell.is_flagged
        return cell.is_flagged

    @property
    def flag_count(self) -> int:
        return sum(cell.is_flagged for cell in self.board.cells())

    @property
    def mine_count(self) -> int:
        return self.board.mine_count

    def is_mine(self, r: int, c: int) -> bool:
        return self.board.get_cell(r, c).is_mine

    def adjacent_count(self, r: int, c: int) -> int:
        return self.board.get_cell(r, c).adjacent

    def is_cleared(self) -> bool:
        for cell in self.board.cells():
            if not cell.is_mine and not cell.is_revealed:
                return False
        return True
