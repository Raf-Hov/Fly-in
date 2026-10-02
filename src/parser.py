def parse_file(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        for i in file:
            if i.startswith("#") or i == "\n":
                continue
            print(f"{i!r}")
    