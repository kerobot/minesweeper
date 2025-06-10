import tkinter as tk
import tkinter.messagebox as msgbox
from .game import MinesweeperGame
from functools import partial


class MinesweeperBoard:
    def __init__(self, rows, cols, cell_size=30, mine_count=10):
        self.game = MinesweeperGame(rows, cols, mine_count)
        self.rows, self.cols, self.cell_size = rows, cols, cell_size
        self.root = tk.Tk()
        self.root.title("Mine-Sweeper")

        # ステータス表示用ラベルを追加（上部）
        self.status_label = tk.Label(
            self.root,
            text=self._make_status_text(),
            anchor="w",
            padx=5,
        )
        self.status_label.grid(row=0, column=0, columnspan=self.cols, sticky="ew")
        # ボタンによる盤面の初期化
        self.buttons = [[None] * cols for _ in range(rows)]
        self._create_widgets()
        self.default_bg = self.buttons[0][0].cget("bg")
        self._configure_grid()
        # 初期モデル＆UI状態をセット
        self._reset_board()

    def _create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.root,
                    width=self.cell_size // 10,
                    height=self.cell_size // 20,
                    command=partial(self.on_left_click, r, c),
                )
                # event 引数を受け取って破棄する
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                btn.grid(row=r + 1, column=c, sticky="nsew")
                self.buttons[r][c] = btn
                self.buttons[r][c] = btn

    def _configure_grid(self):
        # ステータス行は固定、高さ0にしておく
        self.root.grid_rowconfigure(0, weight=0)
        for i in range(self.rows):
            self.root.grid_rowconfigure(i + 1, weight=1)
        for i in range(self.cols):
            self.root.grid_columnconfigure(i, weight=1)

    def _reset_board(self):
        self.game.reset()
        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                btn.config(
                    text="",
                    state=tk.NORMAL,
                    relief=tk.RAISED,
                    fg="black",
                    bg=self.default_bg,
                )
        self._update_status()

    def on_left_click(self, r, c):
        if self.game.is_mine(r, c):
            btn = self.buttons[r][c]
            btn.config(text="💣", fg="red", state=tk.DISABLED, relief=tk.SUNKEN)
            if msgbox.askyesno(
                "ゲームオーバー", "地雷を踏みました。\n新しいゲームを開始しますか？"
            ):
                self._reset_board()
            else:
                self.root.destroy()
        else:
            # モデル側で再帰的に開示処理
            self.game.reveal(r, c)
            # UI をモデルに合わせて更新
            self._refresh_view()
            self._check_win()

    def on_right_click(self, r: int, c: int):
        cell = self.game.board[r][c]
        # 開示済みセルには旗を立てない
        if cell.is_revealed:
            return
        # フラグのON/OFF切り替え
        flag_on = self.game.toggle_flag(r, c)
        btn = self.buttons[r][c]
        if flag_on:
            btn.config(text="🚩", fg="red")  # 旗は赤色で表示！
        else:
            btn.config(text="", fg="black")
        # 旗の数が変わったらステータス更新
        self._update_status()

    def _refresh_view(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.game.board[r][c]
                btn = self.buttons[r][c]
                if cell.is_revealed:
                    # 隣接地雷数に応じて色を変えるよ！
                    if cell.adjacent == 1:
                        num_fg = "blue"
                    elif cell.adjacent == 2:
                        num_fg = "green"
                    elif cell.adjacent >= 3:
                        num_fg = "red"
                    else:
                        num_fg = "black"
                    btn.config(
                        text=str(cell.adjacent) if cell.adjacent > 0 else "",
                        state=tk.DISABLED,
                        relief=tk.SUNKEN,
                        disabledforeground=num_fg,
                        bg="lightgrey",
                    )
                elif cell.is_flagged:
                    btn.config(text="🚩", fg="red")  # 旗は赤色で表示！
                else:
                    btn.config(
                        text="",
                        state=tk.NORMAL,
                        relief=tk.RAISED,
                        fg="black",
                        bg=self.default_bg,
                    )

    def _check_win(self) -> None:
        if self.game.is_cleared():
            if msgbox.askyesno(
                "クリア", "ゲームクリア！\n新しいゲームを開始しますか？"
            ):
                self._reset_board()
            else:
                self.root.destroy()

    def _make_status_text(self) -> str:
        return f"🚩 {self.game.flag_count}  /  💣 {self.game.mine_count}"

    def _update_status(self) -> None:
        self.status_label.config(text=self._make_status_text())

    def run(self):
        self.root.mainloop()
