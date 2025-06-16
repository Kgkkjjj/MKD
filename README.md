# MKD

`mkd.pyoc` demonstrates the same tool using a minimal language called **pyoc**.
It relies only on the Python standard library and is executed with the helper
`pyoc.py` interpreter.

The interpreter supports importing additional `.pyoc` modules from the `lib`
directory. An example module `fs.pyoc` provides basic file‑system utilities.

## Usage

```
python pyoc.py mkd.pyoc <directory>
```

The command creates the specified directory and any required parent
directories if they do not already exist. Modules under `lib` can be
imported in `.pyoc` scripts just like regular Python modules.
