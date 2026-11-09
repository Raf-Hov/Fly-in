"""Interactive menu to pick a map file from the maps/ directory."""
from pathlib import Path


class MapLobby:
    """Lists maps grouped by sub-folder and asks the user to pick one."""

    def __init__(self, maps_dir: Path | None = None) -> None:
        default = Path(__file__).parent.parent / "maps"
        self.maps_dir = maps_dir if maps_dir is not None else default
        self.categories: list[tuple[str, list[Path]]] = []
        self.choices: dict[int, Path] = {}

    def discover(self) -> None:
        if not self.maps_dir.is_dir():
            raise FileNotFoundError(f"maps folder not found: {self.maps_dir}")
        self.categories = []
        self.choices = {}
        number = 1
        for folder in sorted(self.maps_dir.iterdir()):
            if not folder.is_dir():
                continue
            files = sorted(folder.glob("*.txt"))
            if not files:
                continue
            self.categories.append((folder.name, files))
            for file in files:
                self.choices[number] = file
                number += 1

    def display(self) -> None:
        number = 1
        for category, files in self.categories:
            print(f"----{category}----")
            for file in files:
                print(f"{number}: {file.stem}")
                number += 1
            print()
        print("q: Quit\n")
        print("---------------------------")

    def choose(self) -> Path | None:
        self.discover()
        self.display()
        while True:
            try:
                answer = input("Choose one of these files: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if answer.lower() == "q":
                return None
            if answer.isdigit() and int(answer) in self.choices:
                return self.choices[int(answer)]
            print("Invalid choice, try again\n")
