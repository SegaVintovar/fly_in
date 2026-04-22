import sys
from .parsing import parsing


def main() -> None:
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as f:
                config_data = f.read()
                data_4_map = parsing(config_data)
        except Exception as e:
            print(str(e), file=sys.stderr)
    else:
        print("The program is missing congiguration file", file=sys.stderr)
    # create a fleet and a map
