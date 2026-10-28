import random
from collections import deque


class Cell:
    def __init__(self) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
        self.ft = False
        self.path_visited = False

class Maze_generator:
    def __init__(self, width: int, height: int, entry: tuple[int, int], 
                exit: tuple[int, int], output_file: str, perfect: bool = False) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
    def maze_gen(self, seed: int | None = None) -> None:
        """DFSを使ったランダム化バックトラック法による迷路生成。

        Args:
            seed: 乱数の初期値。同じ設定とseedで同じ迷路を再現する。
            Noneの場合は、実行ごとにランダムに生成する。
        """

        random.seed(seed)
        self.grid = [
        [Cell() for _ in range(self.width)]
        for _ in range(self.height)
        ]
        self.stack = [self.entry]

        x, y = self.entry
        self.grid[y][x].visited = True
        self.open_extra = False
        self.extra_open_count = 0

        self.place_42_pattern()
        while self.stack:
            now_x, now_y = self.stack[-1]
            next_grid = self.decide_next(now_x, now_y)

            if next_grid is None:
                self.stack.pop()
                continue

            self.carve_passage(next_grid, now_x, now_y)
            self.stack.append(next_grid)

        if not self.perfect:
            self.open_extra = True
            self.find_dead_ends()
            self.open_extra_passage()
            


    def open_extra_passage(self) -> None:
        """行き止まりのセルに穴をあけ経路を増やす"""
        while self.dead_ends:

            dead_end = self.dead_ends.pop(random.randrange(len(self.dead_ends)))
            dead_x, dead_y = dead_end
            cell = self.grid[dead_y][dead_x]
            wall_count = cell.north + cell.east + cell.south + cell.west
            next_grid = self.decide_next(dead_x, dead_y)

            if next_grid is None or wall_count != 3:
                continue
            
            self.carve_passage(next_grid, dead_x, dead_y)
            self.extra_open_count += 1

    def would_create_open_area(
        self,
        now_x: int,
        now_y: int,
        next_grid: tuple[int, int],
    ) -> bool:
        """壁を壊しても3*3にならないか確かめる。

        Args:
            now_x: 現在地のx座標。
            now_y: 現在地のy座標
            next_grid: 壁を壊す方向のセル

        Returns:
            壁を壊して良いかの判断。
        """
        next_x, next_y = next_grid

        if now_y == next_y:
            opening = (min(now_x, next_x), now_y, "east")
        else:
            opening = (now_x, min(now_y, next_y), "south")

        check_south = [
            (0, 0), (1, 0), (2, 0),
            (0, 1), (1, 1), (2, 1),
        ]
        check_east = [
            (0, 0), (1, 0),
            (0, 1), (1, 1),
            (0, 2), (1, 2),
        ]

        for top_y in range(now_y - 2, now_y + 1):
            for top_x in range(now_x - 2, now_x + 1):
                if (top_x < 0 or top_y < 0
                        or top_x + 2 >= self.width
                        or top_y + 2 >= self.height):
                    continue

                if not (top_x <= next_x <= top_x + 2
                        and top_y <= next_y <= top_y + 2):
                    continue

                wall_remains = False

                for dx, dy in check_south:
                    x = top_x + dx
                    y = top_y + dy

                    if (x, y, "south") == opening:
                        continue

                    if self.grid[y][x].south:
                        wall_remains = True
                        break

                if wall_remains:
                    continue

                for dx, dy in check_east:
                    x = top_x + dx
                    y = top_y + dy

                    if (x, y, "east") == opening:
                        continue

                    if self.grid[y][x].east:
                        wall_remains = True
                        break

                if not wall_remains:
                    return True

        return False
    
    def find_dead_ends(self) -> None:
        """行き止まりのセルの座標をself.dead_endsに保存する。"""
        self.dead_ends = []

        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[y][x]
                wall_count = cell.north + cell.east + cell.south + cell.west
                if wall_count != 3:
                    continue
                self.dead_ends.append((x, y))


    def place_42_pattern(self) -> None:
        """迷路に42模様を設置する。"""

        def can_place_42(
                center: tuple[int, int],
                place_42: list[tuple[int, int]]
        ) -> bool:
            """その場所に42模様を設置して良いか確かめる。

            Args:
                center: 42模様の中心の座標
                place_42: 42模様の設置座標

            Returns:
                centerの場所が適しているかどうかの判断。
            """
            center_x, center_y = center
            if not (4 <= center_x < self.width - 4
                    and 3 <= center_y < self.height - 3):
                return False
            for d_x, d_y in place_42:
                ft_x = center_x + d_x
                ft_y = center_y + d_y
                if (ft_x, ft_y) in (self.entry, self.exit):
                    return False
                if not self.perfect:
                    maze_center = (self.width // 2, self.height // 2)
                    if (ft_x, ft_y) == maze_center:
                        return False
                
            return True
        

        place_42 = [(-1, 0), (-2, 0), (-3, 0), (-3, -1),
                    (-3, -2), (-1, 1), (-1, 2), (1, 0),
                    (2, 0), (3, 0), (3, -1), (3, -2),
                    (2, -2), (1, -2), (1, 1), (1, 2),
                    (2, 2), (3, 2)]
        offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in offsets:
            center_x = self.width // 2 + dx
            center_y = self.height // 2 + dy
            can_place = can_place_42((center_x, center_y), place_42)
            if can_place:
                break

        if not can_place:
            for center_y in range(3, self.height - 3):
                for center_x in range(4, self.width - 4):
                    can_place = can_place_42((center_x, center_y), place_42)

                    if can_place:
                        break
                if can_place:
                    break

        if self.height < 7 or self.width < 9 or not can_place:
            print("Maze too small to include the '42' pattern. Continuing without it.")
            return

        for d_x, d_y in place_42:
            ft_x = center_x + d_x
            ft_y = center_y + d_y

            self.grid[ft_y][ft_x].ft = True
            

    def carve_passage(
            self,
            next_grid: tuple[int, int],
            now_x: int,
            now_y: int
    ) -> None:
        """壁に穴を開ける。

        Args:
            next_grid: 穴を開ける先の座標
            now_x: 現在地のx座標
            now_y: 現在地のy座標
        """
        
        next_x, next_y = next_grid
        direction = (next_x - now_x + 2 * (next_y - now_y))
        now_cell = self.grid[now_y][now_x]
        next_cell = self.grid[next_y][next_x]

        if direction == -2:
            now_cell.north = False
            next_cell.south = False

        elif direction == 1:
            now_cell.east = False
            next_cell.west = False

        elif direction == 2:
            now_cell.south = False
            next_cell.north = False

        elif direction == -1:
            now_cell.west = False
            next_cell.east = False

        next_cell.visited = True

    def decide_next(self,
                    now_x: int,
                    now_y: int
    ) -> tuple[int, int] | None:
        """条件を満たす隣接セルから、ランダムに移動先を選ぶ。
        
        Args:
            now_x: 現在地のx座標
            now_y: 現在地のy座標
        
        Returns:
            選ばれたセルの座標。候補がない場合はNone。
        """

        next_list = []
        checks =[(1, 0), (0, 1), (-1, 0), (0, -1)]

        for d_x, d_y in checks:
            check_x = now_x + d_x
            check_y = now_y + d_y

            if not (0 <= check_x < self.width
                    and 0 <= check_y < self.height):
                continue

            cell = self.grid[check_y][check_x]

            if not self.open_extra:
                if cell.visited:
                    continue

            if cell.ft:
                continue

            if self.open_extra:
                now_cell = self.grid[now_y][now_x]

                if self.would_create_open_area(now_x, now_y, (check_x, check_y)):
                    continue
                if d_x == 1 and not now_cell.east:
                    continue
                if d_x == -1 and not now_cell.west:
                    continue
                if d_y == 1 and not now_cell.south:
                    continue
                if d_y == -1 and not now_cell.north:
                    continue

            next_list.append((check_x, check_y))

        if not next_list:
            return None
        
        return random.choice(next_list)
        
    def find_shortest_path(self) -> list[tuple[int, int]]:
        """BFSによる最短ルート検索。

        Returns:
            最短ルートのリスト
        """
        self.queue = deque([self.entry])
        came_from = {}
        self.grid[self.entry[1]][self.entry[0]].path_visited = True
        shortest_path = []
        current = self.exit

        while self.queue:
            now_x, now_y = self.queue.popleft()
            if (now_x, now_y) == self.exit:
                break

            for next_x, next_y in self.get_accessible_neighbors(now_x, now_y):
                came_from[(next_x, next_y)] = (now_x, now_y)
                self.grid[next_y][next_x].path_visited = True
                self.queue.append((next_x, next_y))

        while current != self.entry:
            shortest_path.append(current)
            current = came_from[current]

        shortest_path.append(self.entry)
        shortest_path.reverse()

        for x in range(self.width):
            for y in range(self.height):
                self.grid[y][x].path_visited = False

        return shortest_path


    def get_accessible_neighbors(
            self,
            now_x: int,
            now_y: int
    ) -> list[tuple[int, int]]:
        """条件を満たす隣接セルを全て選ぶ。

        Args:
            now_x: 現座地のx座標
            now_y: 現在地のy座標

        Returns:
            選ばれたセルのリスト。"""
        checks =[(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []
        now_cell = self.grid[now_y][now_x]
        for x, y in checks:
            next_x = now_x + x
            next_y = now_y + y
            
            if not (0 <= next_x < self.width
                    and 0 <= next_y < self.height):
                continue

            next_cell = self.grid[next_y][next_x]

            if next_cell.ft or next_cell.path_visited:
                continue


            if x == 1 and now_cell.east == False:
                result.append((next_x, next_y))

            if y == 1 and now_cell.south == False:
                result.append((next_x, next_y))

            if x == -1 and now_cell.west == False:
                result.append((next_x, next_y))

            if y == -1 and now_cell.north == False:
                result.append((next_x, next_y))

        return result


    def write_to_file(self) -> None:
        """迷路、最短経路を指定形式でファイルに保存する。 """
        
        shortest_path = self.find_shortest_path()
        try:
            with open(self.output_file, "w") as f:
                for y in range(self.height):
                    for x in range(self.width):
                        cell = self.grid[y][x]
                        value = (
                        cell.north
                        + cell.east * 2
                        + cell.south * 4
                        + cell.west * 8
                        )
                        hex_wall = format(value, "X")
                        f.write(hex_wall)
                    f.write("\n")
                f.write("\n")
                f.write(f"{self.entry[0]},{self.entry[1]}\n")
                f.write(f"{self.exit[0]},{self.exit[1]}\n")
                first_x , first_y = self.entry
                for next_x, next_y in shortest_path[1:]:
                    direction = ((next_x - first_x) +
                                2 * (next_y - first_y))
                    if direction == 1:
                        f.write("E")

                    elif direction == -1:
                        f.write("W")

                    elif direction == 2:
                        f.write("S")

                    elif direction == -2:
                        f.write("N")

                    first_x = next_x
                    first_y = next_y
                f.write("\n")

        except OSError as e:
            print(e)