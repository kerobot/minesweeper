__all__ = ["Board", "Cell"]

from dataclasses import dataclass
from typing import List, Callable, Optional, Set, Tuple
import random


@dataclass
class Cell:
    is_mine: bool = False
    is_revealed: bool = False
    is_flagged: bool = False
    adjacent: int = 0


class Board:
    def __init__(
        self,
        rows: int,
        cols: int,
        mine_count: int,
        *,
        rng: Optional[random.Random] = None,
        preset_mines: Optional[Set[Tuple[int, int]]] = None,
    ):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.rng = rng or random
        self._preset_mines = preset_mines
        self.reset()

    def reset(self) -> None:
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(self.cols)] for _ in range(self.rows)
        ]
        if self._preset_mines is not None:
            for r, c in self._preset_mines:
                self.grid[r][c].is_mine = True
        else:
            self._place_mines()
        self._calc_adjacent_counts()

    def _place_mines(self) -> None:
        placed = 0
        while placed < self.mine_count:
            r = self.rng.randrange(self.rows)
            c = self.rng.randrange(self.cols)
            cell = self.grid[r][c]
            if not cell.is_mine:
                cell.is_mine = True
                placed += 1

    def _calc_adjacent_counts(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                cnt = 0

                def inc_if_mine(nr: int, nc: int):
                    nonlocal cnt
                    if self.grid[nr][nc].is_mine:
                        cnt += 1

                self.for_each_neighbor(r, c, inc_if_mine)
                self.grid[r][c].adjacent = cnt

    def for_each_neighbor(self, r: int, c: int, fn: Callable[[int, int], None]) -> None:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    fn(nr, nc)

    def get_cell(self, r: int, c: int) -> Cell:
        return self.grid[r][c]

    def cells(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def __getitem__(self, idx):
        return self.grid[idx]

    def __len__(self):
        return len(self.grid)

    def __iter__(self):
        return iter(self.grid)
