import sys
from a_maze_ing import Maze_generator


def Loading_config() -> dict[str: int | bool | str | tuple[int, int]]:


    config = {}

    try:
        with open(sys.argv[1], "r") as file:
            config_texts = file.read().splitlines()

            for config_text in config_texts:

                line = config_text.strip()
                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=")
                key = key.strip()
                value = value.strip()

                if key == "OUTPUT_FILE":
                    config[key] = value

                elif key in "PERFECT":
                    try:
                        config[key] = bool(value)
                    except ValueError as e:
                        print(e)

                elif key == "ENTRY" or key == "EXIT":
                    try:
                        config[key] = tuple(int(v) for v in value.split(","))
                    except ValueError as e:
                        print(e)

                else:
                    try:
                        config[key] = int(value)
                    except ValueError as e:
                        print(e)

    except FileNotFoundError as e:
        print(e)

    except PermissionError as e:
        print(e)

    return config

def main() -> None:

    config = Loading_config()
    Maze_gen = Maze_generator()