def input_file(file: str) -> dict:
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

def draw_cell(cell: int, is_last_col: bool, is_last_row: bool, on_path: bool = False) -> list[str]:
    north = (cell >> 0) & 1
    east  = (cell >> 1) & 1
    south = (cell >> 2) & 1
    west  = (cell >> 3) & 1

    top = "+-" if north == 1 else "+ "
    l = "|" if west == 1 else " "
    mark = "." if on_path else " "
    mid = l + mark
    if is_last_col:
        top += "+"
        r = "|" if east == 1 else " "
        mid += r
    if is_last_row:
        bot = "+-" if south == 1 else "+ "
        if is_last_col:
            bot += "+"
    else:
        bot = ""

    return [top, mid, bot]

def draw_maze(maze: list[list[int]], color: str = "\033[37m", path_coords: list[tuple] | None = None) -> None:
    reset = "\033[0m"
    last_row = len(maze) - 1
    last_col = len(maze[0]) - 1
    coords = set(path_coords) if path_coords else set()
    for y, maze_row in enumerate(maze):
        row_top = ""
        row_mid = ""
        row_bot = ""
        for x, cell in enumerate(maze_row):
            is_last_col = (x == last_col)
            is_last_row = (y == last_row)
            on_path = (x, y) in coords
            parts = draw_cell(cell, is_last_col, is_last_row, on_path)
            row_top += parts[0]
            row_mid += parts[1]
            row_bot += parts[2]
        print(color + row_top + reset)
        print(color + row_mid + reset)
        if row_bot:
            print(color + row_bot + reset)

COLORS = ["\033[37m", "\033[31m", "\033[32m", "\033[33m", "\033[34m"]
COLOR_NAMES = ["white", "red", "green", "yellow", "blue"]


def menu(data: dict) -> None:
    show_path = False
    color_index = 0
    maze = data["maze"]
    path_coords = calc_path(data["entry"], data["path"])

    while True:
        coords = path_coords if show_path else None
        draw_maze(maze, COLORS[color_index], coords)
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            pass  # TODO: バックエンドを呼び出して再生成
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(COLORS)
        elif choice == "4":
            break

def calc_path(entry: tuple, path: str) -> list[tuple]:
    moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    coords = [entry]
    x, y = entry
    for ch in path:
        dx, dy = moves[ch]
        x += dx
        y += dy
        coords.append((x, y))
    return coords

