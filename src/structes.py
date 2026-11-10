from dataclasses import dataclass, field
from enum import Enum


class ZoneTypes(Enum):
    """Kinds of zones a map can contain."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    """A node of the network."""

    name: str
    x: int
    y: int
    zone_type: ZoneTypes = ZoneTypes.NORMAL
    color: str | None = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False

    @property
    def move_cost(self) -> int:
        """Turns needed to enter this zone."""
        return 2 if self.zone_type is ZoneTypes.RESTRICTED else 1

    @property
    def capacity(self) -> int | None:
        """Max simultaneous drones; None means unlimited (start/end)."""
        if self.is_start or self.is_end:
            return None
        return self.max_drones


@dataclass
class Connection:
    """A bidirectional edge between two zones."""

    zone1: str
    zone2: str
    max_link_capacity: int = 1

    @property
    def key(self) -> frozenset[str]:
        """Order-independent identity: a-b equals b-a."""
        return frozenset((self.zone1, self.zone2))


@dataclass
class MapData:
    """Fully validated content of a map file."""

    nb_drones: int
    start_hub: Zone
    end_hub: Zone
    zones: dict[str, Zone] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
