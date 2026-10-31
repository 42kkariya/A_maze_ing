import sys
from typing import TypedDict, cast
from mazegen import Mazegenerator
from front import input_file, menu

ConfigValue = int | bool | str | tuple[int, int]


class RequiredConfig(TypedDict):
    """設定ファイルの型ヒント"""
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


class Config(RequiredConfig, total=False):
    """設定ファイルの型ヒント"""
    SEED: int


def loading_config(file_name: str) -> Config:
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

    result = cast(Config, config)

    width = result["WIDTH"]
    height = result["HEIGHT"]
    entry = result["ENTRY"]
    exit = result["EXIT"]

    if (
        entry == exit or
        not result["PERFECT"] and (width < 4 or height < 4) or
        not (0 <= entry[0] < width and 0 <= entry[1] < height)
        or not (0 <= exit[0] < width and 0 <= exit[1] < height)
    ):
        raise ValueError("不正な値が入力されています。")

    return result


def generate(config: Config, seed: int | None) -> dict | None:
    """迷路を生成して OUTPUT_FILE に書き出し、表示用の辞書を返す。

    Args:
        config: loading_config() の返り値。
        seed: 乱数のシード。None なら毎回違う迷路になる。

    Returns:
        input_file() の返り値。書き出したファイルを読み直したもの。
    """
    maze = Mazegenerator(
        config["WIDTH"], config["HEIGHT"],
        config["ENTRY"], config["EXIT"],
        config["OUTPUT_FILE"],
        seed=seed,
        perfect=config["PERFECT"],
    )
    maze.maze_gen()
    maze.write_to_file()
    return input_file(config["OUTPUT_FILE"])


def main() -> None:
    """設定ファイルを読み込み、迷路を生成して表示する。"""
    if len(sys.argv) != 2:
        print("実行方法: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = loading_config(sys.argv[1])
        # 最初の迷路は SEED を使い、再生成のときは毎回違う迷路にする
        data = generate(config, config.get("SEED"))

    except FileNotFoundError:
        print(f"エラー: 設定ファイルが見つかりません: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        print("エラー: 設定ファイルを読み込む権限がありません", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)

    menu(data, lambda: generate(config, None))


if __name__ == "__main__":
    main()
