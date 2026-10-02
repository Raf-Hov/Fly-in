from pathlib import Path, PosixPath


def get_name_of_files() -> list[tuple[str, list[tuple[PosixPath, int]]]]:
    curr_path = Path(__file__).parent.parent / "maps"
    file_list: list[tuple[str, list[tuple[PosixPath, int]]]] = []
    ba: int = 1
    if not curr_path.is_dir():
        raise FileNotFoundError()
    for i in curr_path.iterdir():
        temp_list: list[str] = []
        if i.name == "README.md":
            continue
        for c in i.glob('*.txt'):
            temp_list.append((c, ba))
            ba += 1
        file_list.append((i.name, temp_list))
    return file_list


def visual_lobby() -> str:
    file_list: list[
        tuple[str, list[tuple[PosixPath, int]]]] = get_name_of_files()
    le: int = 0
    b: int = 1
    for _, kv in file_list:
        le += len(kv)
    for i, j in file_list:
        print(f"----{i}----")
        for kv in j:
            am, fm = kv
            while b <= le:
                b += 1
                break
            print(f"{fm}: {am.stem}")
        print()
    le += 1
    print(f"{le}: Quit\n")
    print("---------------------------")
    while True:
        try:
            choosed = int(input("Choose one of these files: "))
            if choosed == le:
                return "dummy"
            for _, vc in file_list:
                for bv in vc:
                    lx, lz = bv
                    if lz == choosed:
                        return str(lx)
            print("Wrong choice try again")
        except ValueError:
            print("Invalid choice \n")
