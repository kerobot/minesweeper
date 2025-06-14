# Mine-Sweeper

## 💖 はじめに 💖

やっほー！これはPythonとTkinterで作ったギャル流マインスイーパーだよ✨
Copilotエージェントと単体テストもバッチリ意識してるから、安心して遊んで＆いじってね！

- `main.py`：アプリのスタート地点！
- `minesweeper/game.py`：ゲームの心臓部！
- `minesweeper/board_core.py`：盤面の管理はここで全部やってるよ！
- `minesweeper/board.py`：UI操作もギャルにおまかせ！

## 🛠️ 環境構築もギャル流で！

VS Code＋pyenv-win＋poetryで開発してるよ！

```powershell
pyenv install 3.13.2
pyenv global 3.13.2
poetry new minesweeper
cd .\minesweeper\
pyenv local 3.13.2 
poetry env use C:\Users\xxxxxxxx\.pyenv\pyenv-win\versions\3.13.2\python.exe
poetry run python -V
# → Python 3.13.2 って出たらOK！
poetry add pytest
code .
```

## クローンして始めるなら？

```powershell
pyenv install 3.13.2
pyenv global 3.13.2
git clone https://github.com/xxxxxxxx/minesweeper.git
cd .\minesweeper\
pyenv local 3.13.2 
poetry env use C:\Users\xxxxxxxx\.pyenv\pyenv-win\versions\3.13.2\python.exe
poetry run python -V
# Python 3.13.2 って出たらイケてる！
poetry install
code .
```

## 🧪 テストもバッチリ！

```powershell
poetry run pytest
```

## 🎮 ゲームを起動しよ！

```powershell
poetry run python src\main.py
```

---

ギャルのマインスイーパーで脳トレしちゃお！バグ見つけたら気軽に教えてね💋
