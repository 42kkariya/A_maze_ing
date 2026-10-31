import sys
from MazeGenerator import Mazegenerator

ConfigValue = int | bool | str | tuple[int, int]


def loading_config(file_name: str) -> dict[str, ConfigValue]:
    """設定ファイルを読み込み、各値を適切な型に変換する。"""
    config: dict[str, ConfigValue] = {}

    with open(file_name, encoding="utf-8") as file:
        for line_number, text in enumerate(file, start=1):
            line = text.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"{line_number}行目: KEY=VALUEの形式で書いてください"
                )

            key, value = [s.strip() for s in line.split("=", 1)]

            if key in config:
                raise ValueError(
                    f"{key}が2つ存在します。"
                )

            if key in ("WIDTH", "HEIGHT", "SEED"):
                try:
                    config[key] = int(value)
                except ValueError as e:
                    raise ValueError(
                        f"{line_number}行目: {key}には整数を指定してください"
                    ) from e

            elif key in ("ENTRY", "EXIT"):
                try:
                    x, y = value.split(",")
                    config[key] = (int(x), int(y))
                except ValueError as e:
                    raise ValueError(
                        f"{line_number}行目: {key}は"
                        "0,0のように整数2個で指定してください"
                    ) from e

            elif key == "PERFECT":
                if value not in ("True", "False"):
                    raise ValueError(
                        f"{line_number}行目: PERFECTは"
                        "TrueかFalseで指定してください"
                    )
                config[key] = value == "True"

            elif key == "OUTPUT_FILE":
                if not value:
                    raise ValueError(
                        f"{line_number}行目: OUTPUT_FILEに"
                        "出力ファイル名を指定してください"
                    )
                config[key] = value

            else:
                raise ValueError(
                    f"{line_number}行目: 未対応のキーです: {key}"
                )

    required = {
        "WIDTH", "HEIGHT", "ENTRY",
        "EXIT", "OUTPUT_FILE", "PERFECT",
    }
    missing = required - config.keys()

    if missing:
        raise ValueError(
            f"必須項目が不足しています: {', '.join(missing)}"
        )

    if (config["ENTRY"] == config["EXIT"] or
        config["HEIGHT"] > 0 or config["WIDTH"] > 0 or
        0 <= config["ENTRY"][0] < config["WIDTH"] or
        0 <= config["ENTRY"][1] < config["HEIGHT"] or
        0 <= config["EXIT"][0] < config["WIDTH"] or
        0 <= config["EXIT"][1] < config["HEIGHT"]):

        raise ValueError("不正な値が入力されています。")


    return config


def main() -> None:
    if len(sys.argv) != 2:
        print("実行方法: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = loading_config(sys.argv[1])
        maze = Mazegenerator(
        config["WIDTH"], config["HEIGHT"],
        config["ENTRY"], config["EXIT"],
        config["OUTPUT_FILE"],
        seed=config.get("SEED"),
        perfect=config["PERFECT"],
        )
        maze.maze_gen()
        maze.write_to_file()

    except FileNotFoundError:
        print(f"エラー: 設定ファイルが見つかりません: {sys.argv[1]}"
              , file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        print("エラー: 設定ファイルを読み込む権限がありません"
              ,file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
