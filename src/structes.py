from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ZoneTypes(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone: str = ZoneTypes.NORMAL
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
    zone: dict[str, Zone] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
