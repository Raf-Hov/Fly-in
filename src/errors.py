class MapParse(Exception):
    def __init__(self, line_num: int, mess: str) -> None:
        self.line_num = line_num
        self.mess = mess
        super().__init__(f"Line {line_num}: {mess}")


class ParsError(Exception):
    def __init__(self, zone: str):
        self.zone = zone
        super().__init__(f"Something wrong with: {zone}")
