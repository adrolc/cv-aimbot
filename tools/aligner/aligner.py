from pathlib import Path

def align(n):
    """
    n - what number to start the alignment with
    """
    path = Path("./images").glob("*")
    files = sorted([x for x in path if x.is_file()], key=lambda path: int(path.stem))
    for i, file in enumerate(files):
        x = i + n
        new_name = file.with_name(str(x)).with_suffix(file.suffix)
        file.rename(new_name)

if __name__ == "__main__":
    align(1)