# MKD

`mkd.pyoc` demonstrates the same tool using a minimal language called **pyoc**.
It relies only on the Python standard library and is executed with the helper `pyoc.py` interpreter.
The interpreter supports importing modules from the `lib` directory and caches them after first load.
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

## Usage

```bash
python pyoc.py mkd.pyoc <directory>
```
Optional flags:
- `--log` to print a creation message
- `--join=<child>` to show a subpath after creation

The command creates the specified directory and any required parent
directories if they do not already exist.
