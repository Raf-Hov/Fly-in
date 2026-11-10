from .errors import ParseError
from .structes import Connection, MapData, Zone, ZoneTypes


class MapParser:
    """Reads a map file and builds a validated MapData."""

    ZONE_PREFIXES = ("start_hub", "end_hub", "hub")
    ZONE_KEYS = ("zone", "color", "max_drones")
    LINK_KEYS = ("max_link_capacity",)

    def __init__(self, filepath: str) -> None:
        """Remember the file to parse."""
        self.filepath = filepath
        self.nb_drones = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self._seen_links: set[frozenset[str]] = set()

    def parse(self) -> MapData:
        """Parse the whole file and return the map."""
        lines = self._read_lines()
        if not lines:
            raise ParseError(0, "file is empty")
        self._parse_nb_drones(*lines[0])
        for number, text in lines[1:]:
            self._parse_line(number, text)
        last = lines[-1][0]
        if self.start_hub is None:
            raise ParseError(last, "missing start_hub")
        if self.end_hub is None:
            raise ParseError(last, "missing end_hub")
        return MapData(self.nb_drones, self.start_hub, self.end_hub,
                       self.zones, self.connections)

    def _read_lines(self) -> list[tuple[int, str]]:
        """Return (line_number, text) for meaningful lines only."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                raw = file.readlines()
        except OSError as err:
            raise ParseError(0, f"cannot read file: {err}") from err
        except UnicodeDecodeError as err:
            raise ParseError(0, f"file is not valid UTF-8: {err}") from err
        lines: list[tuple[int, str]] = []
        for number, line in enumerate(raw, start=1):
            text = line.split("#", 1)[0].strip()
            if text:
                lines.append((number, text))
        return lines

    def _parse_nb_drones(self, number: int, text: str) -> None:
        """Validate the mandatory first line."""
        key, sep, value = text.partition(":")
        if key.strip() != "nb_drones" or not sep:
            raise ParseError(number, "first line must be 'nb_drones: <n>'")
        self.nb_drones = self._positive_int(number, "nb_drones",
                                            value.strip())

    def _parse_line(self, number: int, text: str) -> None:
        """Dispatch a line to the zone or connection parser."""
        prefix, sep, rest = text.partition(":")
        prefix = prefix.strip()
        if not sep:
            raise ParseError(number, f"missing ':' in '{text}'")
        if prefix in self.ZONE_PREFIXES:
            self._parse_zone(number, prefix, rest.strip())
        elif prefix == "connection":
            self._parse_connection(number, rest.strip())
        elif prefix == "nb_drones":
            raise ParseError(number, "nb_drones defined more than once")
        else:
            raise ParseError(number, f"unknown line type '{prefix}'")

    def _split_metadata(
        self, number: int, text: str, allowed: tuple[str, ...]
    ) -> tuple[str, dict[str, str]]:
        """Split 'main [k=v k=v]' into the main part and a dict."""
        start = text.find("[")
        if start == -1:
            if "]" in text:
                raise ParseError(number, "unmatched ']'")
            return text, {}
        if not text.endswith("]"):
            raise ParseError(number, "metadata must end with ']'")
        inner = text[start + 1:-1]
        if "[" in inner or "]" in inner:
            raise ParseError(number, "malformed metadata brackets")
        meta: dict[str, str] = {}
        for token in inner.split():
            key, sep, value = token.partition("=")
            if not sep or not key or not value:
                raise ParseError(number, f"bad metadata entry '{token}'")
            if key not in allowed:
                raise ParseError(number, f"unknown metadata key '{key}'")
            if key in meta:
                raise ParseError(number, f"duplicate metadata key '{key}'")
            meta[key] = value
        return text[:start].strip(), meta

    @staticmethod
    def _positive_int(number: int, name: str, value: str) -> int:
        """Convert value to a strictly positive int."""
        try:
            result = int(value)
        except ValueError:
            raise ParseError(
                number, f"{name} must be an integer, got '{value}'"
            ) from None
        if result <= 0:
            raise ParseError(number, f"{name} must be positive")
        return result

    def _parse_zone(self, number: int, prefix: str, text: str) -> None:
        """Parse a start_hub / end_hub / hub line."""
        main, meta = self._split_metadata(number, text, self.ZONE_KEYS)
        parts = main.split()
        if len(parts) != 3:
            raise ParseError(number, "expected '<name> <x> <y>'")
        name = parts[0]
        if "-" in name:
            raise ParseError(number, f"zone name '{name}' contains a dash")
        if name in self.zones:
            raise ParseError(number, f"duplicate zone name '{name}'")
        try:
            x, y = int(parts[1]), int(parts[2])
        except ValueError:
            raise ParseError(number, "coordinates must be integers") from None
        zone = Zone(name, x, y, is_start=prefix == "start_hub",
                    is_end=prefix == "end_hub")
        if "zone" in meta:
            try:
                zone.zone_type = ZoneTypes(meta["zone"])
            except ValueError:
                raise ParseError(
                    number, f"invalid zone type '{meta['zone']}'"
                ) from None
        zone.color = meta.get("color")
        if "max_drones" in meta and not (zone.is_start or zone.is_end):
            zone.max_drones = self._positive_int(
                number, "max_drones", meta["max_drones"])
        self._register(number, zone)

    def _register(self, number: int, zone: Zone) -> None:
        """Store the zone and enforce unique start / end."""
        if zone.is_start:
            if self.start_hub is not None:
                raise ParseError(number, "more than one start_hub")
            self.start_hub = zone
        if zone.is_end:
            if self.end_hub is not None:
                raise ParseError(number, "more than one end_hub")
            self.end_hub = zone
        self.zones[zone.name] = zone

    def _parse_connection(self, number: int, text: str) -> None:
        """Parse a connection line."""
        main, meta = self._split_metadata(number, text, self.LINK_KEYS)
        names = main.split("-")
        if len(names) != 2 or not all(names):
            raise ParseError(number, "expected '<zone1>-<zone2>'")
        first, second = names
        for name in names:
            if name not in self.zones:
                raise ParseError(number, f"unknown zone '{name}'")
        if first == second:
            raise ParseError(number, "a zone cannot connect to itself")
        link = Connection(first, second)
        if link.key in self._seen_links:
            raise ParseError(
                number, f"duplicate connection '{first}-{second}'")
        if "max_link_capacity" in meta:
            link.max_link_capacity = self._positive_int(
                number, "max_link_capacity", meta["max_link_capacity"])
        self._seen_links.add(link.key)
        self.connections.append(link)
