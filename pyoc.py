import sys
import os
import builtins
import types

LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')
orig_import = builtins.__import__
# simple cache of loaded modules to avoid rereading files
_module_cache = {}


def pyoc_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Import handler that loads .pyoc modules from the lib directory."""
    try:
        return orig_import(name, globals, locals, fromlist, level)
    except ModuleNotFoundError:
        module_path = os.path.join(LIB_DIR, f"{name}.pyoc")
        if not os.path.exists(module_path):
            raise
        if name in _module_cache:
            return _module_cache[name]
        with open(module_path, 'r', encoding='utf-8') as f:
            code = f.read()
        module = types.ModuleType(name)
        module.__file__ = module_path
        sys.modules[name] = module
        exec(compile(code, module_path, 'exec'), module.__dict__)
        _module_cache[name] = module
        return module


builtins.__import__ = pyoc_import


def run_pyoc(path, args):
    """Run a .pyoc file as if it were a Python script."""
    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()
    sys.argv = [path] + args
    globals_dict = {
        "__name__": "__main__",
        "__file__": path,
    }
    exec(compile(code, path, 'exec'), globals_dict)


def run_string(code: str, args):
    """Execute pyoc source code from a string."""
    path = '<string>'
    sys.argv = [path] + args
    globals_dict = {
        "__name__": "__main__",
        "__file__": path,
    }
    exec(compile(code, path, 'exec'), globals_dict)


def list_scripts():
    """List available .pyoc scripts in the current directory."""
    base = os.path.dirname(__file__)
    for name in sorted(os.listdir(base)):
        if name.endswith('.pyoc') and name != 'pyoc.py':
            print(name)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(f"Usage: {sys.argv[0]} <script.pyoc> [args...]")
        print(f"       {sys.argv[0]} --list")
        return
    if sys.argv[1] == '--list':
        list_scripts()
        return
    script = sys.argv[1]
    if not os.path.exists(script):
        if not script.endswith('.pyoc'):
            candidate = script + '.pyoc'
            if os.path.exists(candidate):
                script = candidate
    if not script.endswith('.pyoc') or not os.path.exists(script):
        print(f"Error: script {script} not found")
        return
    run_pyoc(script, sys.argv[2:])


if __name__ == '__main__':
    main()
