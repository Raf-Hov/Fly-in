from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False


@dataclass
class Connection:
    zone1: str
    zone2: str
    max_link_capacity: int = 1


@dataclass
class MapData:
    nb_drones: int
    start_hub: Zone
    end_hub: Zone
    zone: list[Zone] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
