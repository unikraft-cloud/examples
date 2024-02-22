# MariaDB

This examples demonstrates how to use [MariaDB](https://mariadb.org), one of the most popular open source relational databases.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 3306:3306/tls -M 1024 .
```

Get the results of the deployment by first forwarding the port (save the returned PID):

```console
socat tcp-listen:3306,bind=127.0.0.1,fork,reuseaddr openssl:broken-shadow-990cz9og.dal0.kraft.cloud:3306 &
```

Then, run the following command to test that it works:

```console
mysql -h 127.0.0.1 -u root -punikraft mysql <<< "select count(*) from user"
```

To stop the socat process, run:

```console
kill -9 <PID>
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
