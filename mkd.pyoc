import sys
import os


def create_directory(path: str) -> None:
    """Create a directory, including parents, if it does not exist."""
    parts = path.strip().split(os.sep)
    current = ""
    for part in parts:
        if not part:
            continue
        current = os.path.join(current, part)
        if not os.path.exists(current):
            os.mkdir(current)


def main(args):
    if len(args) != 2:
        print(f"Usage: {args[0]} <directory>")
        return
    directory = args[1]
    create_directory(directory)


if __name__ == "__main__":
    main(sys.argv)
