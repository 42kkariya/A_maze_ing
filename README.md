# A-Maze-ing

<!-- TODO: 完成後に、1行目の斜体の一文・Description・アルゴリズム・再利用・チーム・Resources を書く -->

## Instructions

### 必要なもの

- Python 3.10 以上

### インストール

```sh
make install
```

`.venv/` に仮想環境を作り、`requirements.txt` の開発用ツール（flake8 / mypy / pytest / build）を入れます。

### 実行

```sh
make run
# または
python3 a_maze_ing.py config.txt
```

### Makefile のルール

| ルール | 内容 |
|---|---|
| `make install` | 仮想環境を作って依存パッケージを入れる |
| `make run` | `config.txt` を使って実行する |
| `make debug` | pdb を使ってデバッグ実行する |
| `make lint` | flake8 と mypy（課題指定のフラグ）を実行する |
| `make lint-strict` | flake8 と `mypy --strict` を実行する |
| `make build` | pip パッケージ `mazegen-*.whl` をビルドしてルートにコピーする |
| `make clean` | `__pycache__` などのキャッシュを消す |
| `make fclean` | `clean` に加えて仮想環境とビルド成果物も消す |

## 設定ファイル

1行に1つ `KEY=VALUE` の形で書きます。`#` で始まる行はコメントです。

| キー | 必須 | 説明 | 例 |
|---|---|---|---|
| `WIDTH` | ○ | 迷路の横幅（セル数） | `WIDTH=20` |
| `HEIGHT` | ○ | 迷路の高さ（セル数） | `HEIGHT=15` |
| `ENTRY` | ○ | 入口の座標 `x,y` | `ENTRY=0,0` |
| `EXIT` | ○ | 出口の座標 `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | ○ | 出力ファイル名 | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | ○ | 完全迷路にするか（`True` / `False`） | `PERFECT=True` |
| `SEED` | | 乱数のシード。同じ値なら同じ迷路になる。省略すると毎回ランダム | `SEED=42` |

座標の `x` は横方向（左が 0）、`y` は縦方向（上が 0）です。

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

## 画面の見方と操作

迷路を Unicode の罫線で表示します。

| 表示 | 意味 |
|---|---|
| `S`（マゼンタ） | 入口 |
| `G`（シアン） | 出口 |
| `█`（グレー） | 「42」の模様のセル |
| `━` `┃` `┏` など（オレンジの太線） | 最短経路（表示をオンにしたとき） |

表示の下にメニューが出るので、番号を入力して Enter を押します。

| 入力 | 操作 |
|---|---|
| `1` | 新しい迷路を生成して表示する |
| `2` | 最短経路の表示 / 非表示を切り替える |
| `3` | 壁の色を切り替える（白 → 赤 → 緑 → 黄 → 青） |
| `4` | 終了する |

Ctrl-D / Ctrl-C でも `4` と同じように終了します。
