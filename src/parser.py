from .structes import Zone, Connection, MapData
from typing import Optional
from .errors import ParsError
import re
import sys


def _open_file(file_path: str) -> list[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            f = file.readlines()
            return f
    except PermissionError as e:
        print(f"Permission Error {e}")
        sys.exit(2)
    except FileNotFoundError as b:
        print(f"File not Found: {b}")
        sys.exit(2)


class MapParser:
    def __init__(self, filepath: str):
        self.nb_drones: Optional[int] = None
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.seen_connection: set[tuple[str, str]] = set()
        self.file_line: list[str] = _open_file(filepath)
        self.clear_list = self._optimaiser()

    def _optimaiser(self) -> list[str]:
        clear_list: list[str] = []
        for i in self.file_line[:]:
            if not i or i == '\n' or i.startswith("#"):
                continue
            clear_list.append(i.strip())
        return clear_list

    @staticmethod
    def _pref_parser(s: str) -> dict[str, str | tuple[int, int]]:
        zone_dict: dict[str, str | tuple] = {}
        enclose = re.search(r'\[(.*?)\]', s)
        try:
            tem_enc = enclose.group(1)
        except AttributeError:
            raise ParsError('start_hub')
        pa = s.removesuffix(enclose.group())
        da = pa.split(" ")
        zone_dict["name"] = da[0]
        zone_dict["x"] = int(da[1])
        zone_dict["y"] = int(da[2])
        temp_list = tem_enc.split(" ")
        for i in temp_list:
            rp = i.split('=')
            zone_dict[rp[0]] = rp[1]
        return zone_dict

    def _parser(self) -> None:
        self.mapdata: list[str] = []
        self.condata: dict[str, str] = {}
        self.zones: list[Zone] = []
        for i in self.clear_list:
            if i.startswith("nb_drones:"):
                self.mapdata.append(i.split(' ')[1])
            elif i.startswith("start_hub:"):
                rem = i.removeprefix("start_hub: ")
                ad = self._pref_parser(rem)
                atr = Zone(**ad)
                print(atr)
            elif i.startswith("hub: "):
                res = i.removeprefix("hub: ")
                ad = self._pref_parser(res)
                atr = Zone(**ad)
                print(atr)
