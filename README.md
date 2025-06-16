# MKD

`mkd.pyoc` demonstrates the same tool using a minimal language called **pyoc**.
It relies only on the Python standard library and is executed with the helper
`pyoc.py` interpreter.

The interpreter supports importing additional `.pyoc` modules from the `lib`
directory. The library now contains multiple small modules providing common
utilities such as filesystem access, path handling, string helpers, math, and
more. These modules can be imported in `.pyoc` scripts just like regular
Python modules.

## Available modules

- `fs` - filesystem helpers
- `path` - path operations
- `string_utils` - string helpers
- `math_utils` - arithmetic helpers
- `time_utils` - timestamp helper
- `rand` - random number generation
- `json_utils` - read and write JSON files
- `log` - timestamped console logging
- `process` - run shell commands
- `http` - simple HTTP GET requests
- `args` - parse key=value arguments
- `collections_utils` - list utilities
- `env` - environment variable access

## Usage

```bash
python pyoc.py mkd.pyoc <directory>
```

The command creates the specified directory and any required parent
directories if they do not already exist.
