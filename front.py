def input_file(file: str) -> dict | None:
    """迷路ファイルを読み込んで辞書形式で返す。

    Args:
        file: 迷路ファイルのパス。16進数グリッド＋空行＋メタ情報の形式。

    Returns:
        maze, entry, exit_, path を含む辞書。読み込み失敗時は None。
    """
    try:
        with open(file) as f:
            lines = f.read().splitlines()

        blank = lines.index("")
        grid_lines = lines[:blank]
        meta_lines = lines[blank + 1:]

        maze = []
        for line in grid_lines:
            row = [int(c, 16) for c in line]
            maze.append(row)

        ex, ey = meta_lines[0].split(",")
        entry = (int(ex), int(ey))
        xx, xy = meta_lines[1].split(",")
        exit_ = (int(xx), int(xy))
        path = meta_lines[2]

        return {"maze": maze, "entry": entry, "exit": exit_, "path": path}
    except FileNotFoundError:
        print(f"Error: {file} が見つかりません")
        return None
    except ValueError:
        print(f"Error: {file} のフォーマットが不正です")
        return None


def draw_maze(
    maze: list[list[int]],
    color: str = "\033[37m",
    path_coords: list[tuple] | None = None,
    entry: tuple | None = None,
    exit_: tuple | None = None,
) -> None:
    """迷路をUnicodeボックス描画文字でターミナルに表示する。

    各セルのビットエンコード: bit0=北, bit1=東, bit2=南, bit3=西 (1=壁あり)。
    交差点ごとに上下左右4方向の壁を参照して適切なボックス文字を選択する。

    Args:
        maze: 2次元配列。maze[y][x] がセルの壁情報 (16進数1桁)。
        color: ANSIエスケープカラーコード。デフォルトは白。
        path_coords: 最短経路の座標リスト [(x, y), ...]。None なら非表示。
        entry: 入口の座標 (x, y)。S で表示する。None なら印なし。
        exit_: 出口の座標 (x, y)。G で表示する。None なら印なし。
    """
    H = len(maze)
    W = len(maze[0])
    reset = "\033[0m"
    coords = set(path_coords) if path_coords else set()
    # 印の後に壁の色へ戻す
    entry_mark = ENTRY_COLOR + "S" + reset + color
    exit_mark = EXIT_COLOR + "G" + reset + color

    def h_wall(cx: int, cy: int) -> int:
        """交差点 (cx, cy) から右方向への水平壁の有無を返す (1=壁あり)。"""
        if cy == H:
            return (maze[H - 1][cx] >> 2) & 1
        return (maze[cy][cx] >> 0) & 1

    def v_wall(cx: int, cy: int) -> int:
        """交差点 (cx, cy) から下方向への垂直壁の有無を返す (1=壁あり)。"""
        if cx == W:
            return (maze[cy][W - 1] >> 1) & 1
        return (maze[cy][cx] >> 3) & 1

    corners = {
        (0, 0, 0, 0): " ", (1, 0, 0, 0): "╴",
        (0, 1, 0, 0): "╶", (1, 1, 0, 0): "─",
        (0, 0, 1, 0): "╵", (1, 0, 1, 0): "┘",
        (0, 1, 1, 0): "└", (1, 1, 1, 0): "┴",
        (0, 0, 0, 1): "╷", (1, 0, 0, 1): "┐",
        (0, 1, 0, 1): "┌", (1, 1, 0, 1): "┬",
        (0, 0, 1, 1): "│", (1, 0, 1, 1): "┤",
        (0, 1, 1, 1): "├", (1, 1, 1, 1): "┼",
    }

    for cy in range(H + 1):
        corner_row = ""
        for cx in range(W + 1):
            left = h_wall(cx - 1, cy) if cx > 0 else 0
            right = h_wall(cx, cy) if cx < W else 0
            up = v_wall(cx, cy - 1) if cy > 0 else 0
            down = v_wall(cx, cy) if cy < H else 0
            corner_row += corners[(left, right, up, down)]
            if cx < W:
                corner_row += "─" if h_wall(cx, cy) else " "
        print(color + corner_row + reset)
        if cy < H:
            cell_row = ""
            for cx in range(W + 1):
                cell_row += "│" if v_wall(cx, cy) else " "
                if cx < W:
                    if (cx, cy) == entry:
                        cell_row += entry_mark
                    elif (cx, cy) == exit_:
                        cell_row += exit_mark
                    elif (cx, cy) in coords:
                        cell_row += "·"
                    else:
                        cell_row += " "
            print(color + cell_row + reset)


COLORS = ["\033[37m", "\033[31m", "\033[32m", "\033[33m", "\033[34m"]
COLOR_NAMES = ["white", "red", "green", "yellow", "blue"]
ENTRY_COLOR = "\033[1;35m"
EXIT_COLOR = "\033[1;36m"


def menu(data: dict | None) -> None:
    """インタラクティブメニューを表示し、ユーザー操作を受け付けるループ。

    Args:
        data: input_file() の返り値。maze, entry, exit_, path を含む辞書。
            読み込み失敗時の None も受け付け、エラーを表示して終了する。
    """
    if data is None:
        print("Error: 迷路データの読み込みに失敗しました")
        return
    show_path = False
    color_index = 0
    maze = data["maze"]
    path_coords = calc_path(data["entry"], data["path"])

    while True:
        coords = path_coords if show_path else None
        draw_maze(
            maze, COLORS[color_index], coords, data["entry"], data["exit"]
        )
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl-D / Ctrl-C は Quit と同じ扱いにする
            print()
            break

        if choice == "1":
            pass  # TODO: バックエンドを呼び出して再生成
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(COLORS)
        elif choice == "4":
            break
        else:
            print("Error:  無効な入力です。1-4の数字で選択してください")


def calc_path(entry: tuple, path: str) -> list[tuple]:
    """経路文字列から座標リストを生成する。

    Args:
        entry: 開始座標 (x, y)。
        path: N/E/S/W の方向文字列 (例: "EESS")。

    Returns:
        経路上の座標リスト [(x, y), ...]。entry を含む。
    """
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    coords = [entry]
    x, y = entry
    for ch in path:
        dx, dy = moves[ch]
        x += dx
        y += dy
        coords.append((x, y))
    return coords
