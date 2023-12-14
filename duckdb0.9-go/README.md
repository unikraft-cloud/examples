# DuckDB Go Example

This directory contains a simple Go example using the [DuckDB](https://duckdb.org) library running with Unikraft in binary compatibility mode.
The Go program is extracted from [DuckDB examples](https://duckdb.org/docs/api/go) and it creates and uses a test database.

## Quick Run

Use `kraft` to run the image:

```console
kraft run -M 192M
```

Once executed, it will print out information from the created database:

```text
id: 42 name: John
```

## Scripted Run

Use the scripted runs, detailed in the common `../README.md`.
Running the scripts will print out information ame as above.
