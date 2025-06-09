from dataclasses import dataclass
from typing import List, Callable, Optional, Set, Tuple
import random


@dataclass
class Cell:
    is_mine: bool = False  # 地雷かどうか
    is_revealed: bool = False  # 開かれたかどうか
    is_flagged: bool = False  # 旗が立っているかどうか
    adjacent: int = 0  # 隣接する地雷の数


class MinesweeperGame:
    def __init__(
        self,
        rows: int,
        cols: int,
        mine_count: int,
        *,
        rng: Optional[random.Random] = None,
        preset_mines: Optional[Set[Tuple[int, int]]] = None
    ):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        # テスト用に外部から Random を渡せる
        self.rng = rng or random
        # テスト用に地雷の位置を固定できる
        self._preset_mines = preset_mines
        self.reset()

    def reset(self) -> None:
        # 盤面セルの初期化
        self.board: List[List[Cell]] = [
            [Cell() for _ in range(self.cols)] for _ in range(self.rows)
        ]
        # preset_mines があればそれを使い、なければランダム配置
        if self._preset_mines is not None:
            for r, c in self._preset_mines:
                self.board[r][c].is_mine = True
        else:
            self._place_mines()
        self._calc_adjacent_counts()

    def _place_mines(self) -> None:
        placed = 0
        while placed < self.mine_count:
            r = self.rng.randrange(self.rows)
            c = self.rng.randrange(self.cols)
            cell = self.board[r][c]
            if not cell.is_mine:
                cell.is_mine = True
                placed += 1

    def _calc_adjacent_counts(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                cnt = 0

                def inc_if_mine(nr: int, nc: int):
                    nonlocal cnt
                    if self.board[nr][nc].is_mine:
                        cnt += 1

                self.for_each_neighbor(r, c, inc_if_mine)
                self.board[r][c].adjacent = cnt

    def for_each_neighbor(self, r: int, c: int, fn: Callable[[int, int], None]) -> None:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    fn(nr, nc)

    def reveal(self, r: int, c: int) -> None:
        cell = self.board[r][c]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.adjacent == 0 and not cell.is_mine:
            self.for_each_neighbor(r, c, lambda nr, nc: self.reveal(nr, nc))

    def toggle_flag(self, r: int, c: int) -> bool:
        cell = self.board[r][c]
        if cell.is_revealed:
            return False
        cell.is_flagged = not cell.is_flagged
        return cell.is_flagged

    @property
    def flag_count(self) -> int:
        return sum(cell.is_flagged for row in self.board for cell in row)

    def is_mine(self, r: int, c: int) -> bool:
        return self.board[r][c].is_mine

    def adjacent_count(self, r: int, c: int) -> int:
        return self.board[r][c].adjacent

    def is_cleared(self) -> bool:
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
