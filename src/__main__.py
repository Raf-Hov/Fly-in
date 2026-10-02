from .lobby_vizual import visual_lobby
from .parser import parse_file


def main() -> None:
    file_path = visual_lobby()
    if file_path == "dummy":
        print("Process interrupted")
        return
    parse_file(file_path)


if __name__ == "__main__":
    main()
