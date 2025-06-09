import sys
import os

# conftest.py で src フォルダをパスに追加していることに注意
from minesweeper.game import MinesweeperGame


# テスト用ゲーム生成関数
def make_game(rows, cols, mine_count, preset_mines=None):
    return MinesweeperGame(rows, cols, mine_count, preset_mines=preset_mines)


def test_地雷を踏んだ時に対象のセルだけが開かれること():
    mines = {(0, 0)}
    game = MinesweeperGame(2, 2, 1, preset_mines=mines)
    # 地雷を踏んだセルだけが開かれる
    game.reveal(0, 0)
    assert game.board[0][0].is_revealed
    # 他のセルは開かれない
    assert not game.board[0][1].is_revealed
    assert not game.board[1][0].is_revealed
    assert not game.board[1][1].is_revealed


def test_すべての地雷にフラグを立てたとき地雷以外を開いたらクリアとなること():
    mines = {(0, 0), (1, 1)}
    game = MinesweeperGame(2, 2, 2, preset_mines=mines)
    # すべての地雷にフラグを立ててもクリアにはならない
    game.toggle_flag(0, 0)
    game.toggle_flag(1, 1)
    assert not game.is_cleared()
    # 地雷以外をすべて開いたらクリアとなる
    game.reveal(0, 1)
    game.reveal(1, 0)
    assert game.is_cleared()


def test_フラグを立てたセルは開けないこと():
    game = MinesweeperGame(2, 2, 0)
    game.toggle_flag(0, 0)
    game.reveal(0, 0)
    assert not game.board[0][0].is_revealed


def test_まわりがすべて地雷の場合の隣接地雷数は8になること():
    mines = {(r, c) for r in range(3) for c in range(3)}
    game = MinesweeperGame(3, 3, 9, preset_mines=mines)
    assert game.board[1][1].adjacent == 8


def test_地雷ゼロの盤面で全セルを開けた時にクリアとなること():
    game = MinesweeperGame(2, 2, 0)
    game.reveal(0, 0)
    assert game.is_cleared()
    for r in range(2):
        for c in range(2):
            assert game.board[r][c].is_revealed


def test_フラグのカウントが正しく増減すること():
    game = MinesweeperGame(2, 2, 0)
    game.toggle_flag(0, 0)
    game.toggle_flag(1, 1)
    game.toggle_flag(0, 0)  # 外す
    assert game.flag_count == 1


def test_リセット時に地雷数が正しく設定されること():
    game = MinesweeperGame(4, 4, 5)
    mines_before = sum(cell.is_mine for row in game.board for cell in row)
    game.reset()
    mines_after = sum(cell.is_mine for row in game.board for cell in row)
    assert mines_before == 5
    assert mines_after == 5


def test_生成した盤面サイズが正しいこと():
    game = make_game(5, 7, 3)
    assert len(game.board) == 5
    assert all(len(row) == 7 for row in game.board)


def test_プリセットした地雷配置が正しいこと():
    mines = {(0, 0), (1, 1), (2, 2)}
    game = make_game(3, 3, 3, preset_mines=mines)
    for r in range(3):
        for c in range(3):
            if (r, c) in mines:
                assert game.board[r][c].is_mine
            else:
                assert not game.board[r][c].is_mine


def test_隣接地雷数の計算が正しいこと():
    mines = {(0, 0)}
    game = make_game(2, 2, 1, preset_mines=mines)
    assert game.board[0][0].adjacent == 0
    assert game.board[0][1].adjacent == 1
    assert game.board[1][0].adjacent == 1
    assert game.board[1][1].adjacent == 1


def test_セルを開けた時に対象のセルだけ開かれること():
    mines = {(0, 0)}
    game = make_game(2, 2, 1, preset_mines=mines)
    game.reveal(1, 1)
    assert game.board[1][1].is_revealed
    assert not game.board[0][0].is_revealed


def test_セルを開けたときに連鎖的に開かれること():
    # 3x3, mine at (0,0), reveal (2,2) should open all except (0,0)
    mines = {(0, 0)}
    game = make_game(3, 3, 1, preset_mines=mines)
    game.reveal(2, 2)
    for r in range(3):
        for c in range(3):
            if (r, c) == (0, 0):
                assert not game.board[r][c].is_revealed
            else:
                assert game.board[r][c].is_revealed


def test_フラグのONOFFが正しく反映されること():
    game = make_game(2, 2, 0)
    assert not game.board[0][0].is_flagged
    assert game.toggle_flag(0, 0)
    assert game.board[0][0].is_flagged
    assert not game.toggle_flag(0, 0)
    assert not game.board[0][0].is_flagged


def test_開いたセルにフラグを立てられないこと():
    game = make_game(2, 2, 0)
    game.reveal(0, 0)
    assert not game.toggle_flag(0, 0)
    assert not game.board[0][0].is_flagged


def test_地雷の存在と隣接地雷数が正しく判定されること():
    mines = {(1, 1)}
    game = make_game(2, 2, 1, preset_mines=mines)
    assert game.is_mine(1, 1)
    assert not game.is_mine(0, 0)
    assert game.adjacent_count(0, 0) == 1


def test_リセット時に盤面が正しく初期化されること():
    mines = {(0, 0)}
    game = make_game(2, 2, 1, preset_mines=mines)
    game.reveal(1, 1)
    game.toggle_flag(0, 0)
    game.reset()
    for r in range(2):
        for c in range(2):
            assert not game.board[r][c].is_revealed
            assert not game.board[r][c].is_flagged
    assert game.board[0][0].is_mine
