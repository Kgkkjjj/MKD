import sys


def run_pyoc(path, args):
    """Run a .pyoc file as if it were a Python script."""
    with open(path, 'r') as f:
        code = f.read()
    sys.argv = [path] + args
    globals_dict = {
        "__name__": "__main__",
        "__file__": path,
    }
    exec(compile(code, path, 'exec'), globals_dict)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <script.pyoc> [args...]")
        return
    script = sys.argv[1]
    if not script.endswith('.pyoc'):
        print("Error: script must have a .pyoc extension")
        return
    run_pyoc(script, sys.argv[2:])


if __name__ == '__main__':
    main()
