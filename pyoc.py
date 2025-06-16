import sys
import os
import builtins
import types

LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')

orig_import = builtins.__import__


def pyoc_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Import handler that loads .pyoc modules from the lib directory."""
    try:
        return orig_import(name, globals, locals, fromlist, level)
    except ModuleNotFoundError:
        module_path = os.path.join(LIB_DIR, f"{name}.pyoc")
        if not os.path.exists(module_path):
            raise
        with open(module_path, 'r') as f:
            code = f.read()
        module = types.ModuleType(name)
        module.__file__ = module_path
        sys.modules[name] = module
        exec(compile(code, module_path, 'exec'), module.__dict__)
        return module


builtins.__import__ = pyoc_import


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
