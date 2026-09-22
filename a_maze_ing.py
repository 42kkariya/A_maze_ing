import sys



def Loading_config() -> dict[str: int | bool | str]:


    config = {}

    try:
        with open(sys.argv[1], "r") as file:
            config_texts = file.read().splitlines()

            for config_text in config_texts:
                if config_text in "#":
                    continue

                key, value = config_text("=")

                if key in "OUTPUT_FILE":
                    config[key] = value

                elif key in "PERFECT":
                    try:
                        config[key] = bool(value)
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
