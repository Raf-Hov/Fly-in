from .lobby_vizual import visual_lobby
from .parser import MapParser
import sys


def main() -> None:
    file_path = visual_lobby()
    if file_path == "dummy":
        print("Process interrupted")
        sys.exit(1)
    mapp = MapParser(file_path)
    mapp._parser()


if __name__ == "__main__":
    main()
