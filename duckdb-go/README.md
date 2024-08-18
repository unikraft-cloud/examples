# DuckDB using Go SDK

[DuckDB](https://duckdb.org) is an in-process SQL OLAP database management system, in your Go project.

To run DuckDB on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will build and deploy the files under `src/`.

After deploying, you can query the service using the provided URL.

## Learn more

- [DuckDB's Go driver](https://duckdb.org/docs/api/go)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
