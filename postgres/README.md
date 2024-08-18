# PostgreSQL

[PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database system.

To run PostgreSQL on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 1024 -e POSTGRES_PASSWORD=unikraft -p 5432:5432/tls .
```

After deploying, you can query the service using the provided URL.
For that, first use `socat` to open a TLS connection (save the returned PID):

```console
socat tcp-listen:5432,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.cloud:5432 &
```

where `<NAME>.<METRO>.kraft.cloud` is the name of the instance created above.

Now you can query PostgreSQL using [`psql`](https://www.postgresql.org/docs/current/app-psql.html).
We assume the username is `postgres` and the password is `unikraft`:

```console
psql -U postgres -h localhost
```

Use the `unikraft` password at the password prompt.
Use SQL and `psql` commands for your work.

To stop the `socat` process, run:

```console
kill -9 <PID>
```

## Using Volumes

You can use volumes for data persistence for you PostgreSQL instance.

For that you would first create a volume:

```console
kraft cloud volume create --name postgres --size 200
```

Then start the PostgreSQL instance and mount that volume:

```console
kraft cloud deploy --metro fra0 -M 1024 -e POSTGRES_PASSWORD=unikraft -e PGDATA=/volume/postgres -v postgres:/volume -p 5432:5432/tls .
```

## Connecting Other Instances to PostgreSQL

It's likely you would want to connect a frontend application (such as a website) to a PostgreSQL instance.
See an example on that in the [FerretDB documentation](../ferretdb/README.md).

## Learn more

- [PostgreSQL's Documentation](https://www.postgresql.org/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
