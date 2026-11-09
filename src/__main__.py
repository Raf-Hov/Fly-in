"""Entry point of the Fly-in simulator."""
import sys

from .errors import ParseError
from .lobby_vizual import MapLobby
from .parser import MapParser


def main() -> None:
    """Ask for a map, parse it and report the result."""
    try:
        chosen = MapLobby().choose()
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    if chosen is None:
        print("Goodbye")
        sys.exit(0)
    try:
        data = MapParser(str(chosen)).parse()
    except ParseError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(data.zones)} zones, {len(data.connections)} "
          f"connections, {data.nb_drones} drones")


if __name__ == "__main__":
    main()
