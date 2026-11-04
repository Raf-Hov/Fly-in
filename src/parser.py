from .structes import Zone, Connection, MapData
from typing import Optional
from .errors import ParsError, DubError
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
        self.mapdata: dict[
            str, Zone | int | dict[str, Zone] | list[Connection]] = []

    def _optimaiser(self) -> list[str]:
        clear_list: list[str] = []
        for i in self.file_line[:]:
            if not i or i == '\n' or i.startswith("#"):
                continue
            clear_list.append(i.strip())
        return clear_list

    def _pref_parser(self, s: str) -> dict[str, str | tuple[int, int] | bool | int]:
        tem = s.split(":")
        tas = tem[0]
        temp = tem[0] + ": "
        wtho_pref = s.removeprefix(temp)
        zone_dict: dict[str, str | tuple[int, int] | bool] = {}
        enclose = re.search(r'\[(.*?)\]', wtho_pref)
        try:
            tem_enc = enclose.group(1)
        except AttributeError:
            raise ParsError(tas)
        pa = wtho_pref.removesuffix(enclose.group())
        da = pa.split(" ")
        zone_dict["name"] = da[0]
        if da[0] in self.zone_names:
            raise DubError(da[0])
        self.zone_names.add(da[0])
        zone_dict["x"] = int(da[1])
        zone_dict["y"] = int(da[2])
        temp_list = tem_enc.split(" ")
        for i in temp_list:
            rp = i.split('=')
            zone_dict[rp[0]] = rp[1]
        if tas.startswith("start_hub"):
            zone_dict["is_start"] = True
        elif tas.startswith("end_hub"):
            zone_dict["is_end"] = True
        zone_dict["max_drones"] = int(zone_dict.get("max_drones", 1))
        return zone_dict

    def _conection_maker(zones: list[Zone], mf_str: str) -> None:
        tem_str = mf_str.removeprefix("connection: ")
        enclose = re.search(r'\[(.*?)\]', tem_str)
        try:
            tem_enc = enclose.group(1)
        except AttributeError:
            raise ParsError(tas)


    def _parser(self) -> None:
        self.condata: list = []
        self.zone_names: set[str] = {}
        self.zones: list[Zone] = []
        for i in self.clear_list:
            if i.startswith("nb_drones:"):
                self.mapdata.append(i.split(' ')[1])
            elif not i.startswith("connection:"):
                ad = self._pref_parser(i)
                self.zones.append(Zone(**ad))
            elif i.startswith("connection:"):
                self._conection_maker(self.zones, i)
                
            else:
                raise ParsError(i)
                
