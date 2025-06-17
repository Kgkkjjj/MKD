# MKD

`mkd.pyoc` demonstrates the same tool using a minimal language called **pyoc**.
It relies only on the Python standard library and is executed with the helper `pyoc.py` interpreter.
The interpreter supports importing modules from the `lib` directory and caches them after first load.
It also includes a `run_string` helper so `.pyoc` source can be executed directly from memory.
Running `pyoc.py --list` prints all available command scripts.
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
- `cli` - helpers for displaying usage
- `collections_utils` - list utilities
- `env` - environment variable access
- `csv_utils` - read and write CSV files
- `xml_utils` - parse and write XML documents
- `config` - simple INI configuration helpers
- `regex_utils` - regular expression helpers
- `net` - hostname lookup and ping
- `file_utils` - copy, move and delete files
- `text_utils` - text formatting helpers
- `date_utils` - date formatting and parsing
- `uuid_utils` - generate UUID strings
- `compression` - gzip compression utilities
- `hashing_utils` - SHA-256 hashing
- `itertools_utils` - extra iterators
- `array_utils` - list chunking and unique helpers
- `decimal_utils` - decimal arithmetic
- `encoding_utils` - base64 and hex conversions
- `html_utils` - HTML escaping helpers
- `os_utils` - wrappers for os operations
- `stats_utils` - basic statistics
- `cache_utils` - memory cache
- `debug` - debug printing
- `file_ext` - extra file helpers
- `parse_utils` - simple text parsing
- `db_utils` - tiny in-memory database
- `queue_utils` - simple queue class
- `url_utils` - build and parse URLs
- `dns_utils` - hostname/IP lookups
- `port_scan` - check if a TCP port is open
- `tcp_server` - one-shot TCP echo server
- `tcp_client` - TCP client utility
- `udp_server` - one-shot UDP echo server
- `udp_client` - UDP client helper
- `ftp_utils` - list directories on an FTP server
- `smtp_utils` - send an email via SMTP
- `ssl_utils` - create SSL contexts
- `socket_utils` - create sockets
- `ssh_client` - test SSH connectivity
- `netstat` - query local network info
- `buffer_io` - in-memory byte streams
- `binary_io` - convert integers and bytes
- `stream_utils` - read lines from streams
- `file_lock` - simple file locking
- `temp_files` - make temporary files
- `async_io` - asynchronous file reads
- `file_monitor` - wait for file changes
- `serializer` - save and load objects

## Command line tools

These scripts can be executed with `python pyoc.py <tool>.pyoc`:
- `echo.pyoc` - print arguments
- `cat.pyoc` - output a file's contents
- `wc.pyoc` - count lines, words and bytes
- `head.pyoc` - show the first lines of a file
- `tail.pyoc` - show the last lines of a file
- `ls.pyoc` - list directory entries
- `touch.pyoc` - create or update a file
- `rm.pyoc` - remove a file or directory
- `cp.pyoc` - copy a file
- `mv.pyoc` - move or rename a file
- `mkdir.pyoc` - create directories
- `grep.pyoc` - search for text in a file

- `pwd.pyoc` - print the current directory
- `date.pyoc` - show the current date and time
- `basename.pyoc` - display a path\'s basename
- `dirname.pyoc` - display a path\'s directory
- `sort.pyoc` - sort lines of a file
- `uniq.pyoc` - filter duplicate lines
- `rev.pyoc` - reverse lines of a file
- `count.pyoc` - count substring occurrences
- `sleep.pyoc` - pause execution
- `whoami.pyoc` - show the current user
- `env.pyoc` - print an environment variable
- `calc.pyoc` - evaluate a Python expression

Use `python pyoc.py --list` to see all available commands. Every tool accepts
`--help` to print its usage.

## Usage

```bash
python pyoc.py mkd.pyoc <directory>
```
Optional flags:
- `--log` to print a creation message
- `--join=<child>` to show a subpath after creation

The command creates the specified directory and any required parent
directories if they do not already exist.

## Systx language

`systx.py` interprets files written in a tiny custom syntax. Each line begins
with a command followed by arguments. Available commands are:

- `set <var> <value>` – assign a number or string to a variable
- `add <a> <b> <dest>` – add two numbers and store the result
- `sub <a> <b> <dest>` – subtract two numbers and store the result
- `mul <a> <b> <dest>` – multiply two numbers
- `div <a> <b> <dest>` – integer divide two numbers
- `mod <a> <b> <dest>` – remainder after dividing
- `read <var>` – read a line from standard input into a variable
- `print <values...>` – print one or more values or quoted strings
- `inc <var>` – increment a variable by 1
- `dec <var>` – decrement a variable by 1
- `and <a> <b> <dest>` – boolean AND storing 1 or 0
- `or <a> <b> <dest>` – boolean OR storing 1 or 0
- `not <a> <dest>` – boolean NOT storing 1 or 0
- `concat <a> <b> <dest>` – concatenate two strings
- `len <value> <dest>` – store the length of a string
- `rand <max> <dest>` – random integer from 0 to `max-1`
- `sleep <seconds>` – pause execution for the given time
- `copy <src> <dest>` – copy a value to another variable
- `push <value>` – push a value onto a stack
- `pop <dest>` – pop a value from the stack into a variable
- `swap <a> <b>` – exchange values of two variables
- `:label` – mark a jump target
- `goto <label>` – jump to a label
- `if <a> <op> <b> goto <label>` – conditional jump using `==`, `!=`, `<`, `>`, `<=`, `>=`
- `func <name>` ... `end` – define a function
- `call <name>` – execute a function
- `return` – return from a function
- `exit` – stop execution immediately

Run a script with:

```bash
python systx.py demo.systx
```

The `demo.systx` script demonstrates looping with labels and conditional jumps.
It also shows the `rand` and `dec` commands.
