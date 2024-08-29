# MariaDB

[MariaDB](https://mariadb.org/) is one of the most popular open source relational databases.

To run MariaDB on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 3306:3306/tls -M 1024 .
```

Get the results of the deployment by first forwarding the port (save the returned PID):

```console
socat tcp-listen:3306,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.host:3306 &
```

Then, run the following command to test that it works:

```console
mysql -h 127.0.0.1 -u root -punikraft mysql <<< "select count(*) from user"
```

To stop the `socat` process, run:

```console
kill -9 <PID>
```

## Learn more

- [MariaDB's Documentation](https://mariadb.org/documentation/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
