# FerretDB

[FerretDB](https://www.ferretdb.com/) is an open-source proxy that translates MongoDB wire protocol queries to SQL.

To run FerretDB on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

To deploy it, you need to deploy a [PostgreSQL instance](https://github.com/kraftcloud/examples/tree/main/postgres16.2) using the `examples` repository:

```console
kraft cloud deploy --metro fra0 --start -M 1024 -e POSTGRES_PASSWORD=unikraft --name postgres .
```

After deploying PostgreSQL, assuming the internal URL is `postgres.internal`, deploy FerretDB.
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 512 -p 27017:27017/tls -e FERRETDB_HANDLER=pg -e FERRETDB_POSTGRESQL_URL=postgres://postgres.internal:5432 -e FERRETDB_LISTEN_ADDR=0.0.0.0:27017 .
```

The command will build and deploy a FerretDB instance, that expects connection on port `27017` using TLS.

After deploying, you can query the service using the provided URL.
For that, first use `socat` to open a TLS connection (save the returned PID):

```console
socat tcp-listen:27017,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.cloud:27017 &
```

Now you can query FerretDB using `mongosh`.
We assume the username is `postgres` and the password is `unikraft`:

```console
mongosh mongodb://postgres:unikraft@127.0.0.1?authMechanism=PLAIN
```

To stop the `socat` process, run:

```console
kill -9 <PID>
```

## Learn more

- [FerretDB's Documentation](https://docs.ferretdb.io/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
