# Mine-Sweeper

## はじめに

Python + Tkinter で開発したマインスイーパーです。
単体テストの組み込みを意識して作ってみました。

- main.py アプリケーションのエントリポイント
- minesweeper/game.py ゲーム本体
- minesweeper/board.py UI操作

## 環境構築

```powershell
> pyenv install 3.13.2
> pyenv global 3.13.2
> poetry new minesweeper
> cd .\minesweeper\
> pyenv local 3.13.2 
> poetry env use C:\Users\xxxxxxxx\.pyenv\pyenv-win\versions\3.13.2\python.exe
> poetry run python -V
Python 3.13.2
> poetry add pytest
> code .
```

## クローンした場合

```powershell
> pyenv install 3.13.2
> pyenv global 3.13.2
> git clone https://github.com/xxxxxxxx/minesweeper.git
> cd .\minesweeper\
> pyenv local 3.13.2 
> poetry env use C:\Users\xxxxxxxx\.pyenv\pyenv-win\versions\3.13.2\python.exe
> poetry run python -V
Python 3.13.2
> poetry install
> code .
```

## テストの実行

```powershell
> poetry run pytest
```

## プログラムの実行

```powershell
> poetry run python src\main.py
```
