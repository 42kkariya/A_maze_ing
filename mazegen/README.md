# mazegen

迷路を生成し、最短経路を求める再利用可能なモジュールです。


## インストール

```sh
pip install mazegen-1.0.0-py3-none-any.whl
```

## 基本の使い方

```python
from mazegen import Mazegenerator

maze = Mazegenerator(20, 15, (0, 0), (19, 14), "maze.txt")
maze.maze_gen()
maze.write_to_file()
```

## パラメータ

```python
Mazegenerator(width, height, entry, exit, output_file, *, seed=None, perfect=False)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `width` | `int` | 迷路の横幅（セル数） |
| `height` | `int` | 迷路の高さ（セル数） |
| `entry` | `tuple[int, int]` | 入口の座標 `(x, y)` |
| `exit` | `tuple[int, int]` | 出口の座標 `(x, y)` |
| `output_file` | `str` | `write_to_file()` の書き出し先 |
| `seed` | `int \| None` | 乱数のシード。同じ値なら同じ迷路になる。`None` なら毎回違う迷路 |
| `perfect` | `bool` | `True` なら完全迷路（入口から出口までの道が1本）。`False` ならループのある迷路 |

`seed` と `perfect` はキーワード引数で渡します。

```python
maze = Mazegenerator(30, 20, (0, 0), (29, 19), "out.txt", seed=42, perfect=True)
```

## 生成した迷路を取り出す

`maze_gen()` を呼んだあと、`maze.grid` に迷路が入ります。`maze.grid[y][x]` が座標 `(x, y)` のセル（`Cell`）です。

```python
cell = maze.grid[0][0]
cell.north, cell.east, cell.south, cell.west   # True なら壁がある
cell.ft                                         # True なら「42」の模様のセル
```

## 最短経路を取り出す

```python
path = maze.find_shortest_path()
# [(0, 0), (1, 0), (1, 1), ..., (19, 14)]  入口から出口までの座標のリスト
```

## ファイルに書き出す

`write_to_file()` は、迷路を1セル16進数1桁（北=1, 東=2, 南=4, 西=8 の壁があるビットを足した値）で書き、空行のあとに入口・出口の座標と最短経路（`N` / `E` / `S` / `W`）を書きます。
