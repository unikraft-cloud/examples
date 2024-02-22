# Memcached

This examples demonstrates how to use [Memcached](https://memcached.org), n in-memory key-value store for small chunks of arbitrary data (strings, objects) from results of database calls, API calls, or page rendering.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 11211:11211/tls -M 256 .
```

Get the results of the deployment by first forwarding the port (save the returned PID):

```console
socat tcp-listen:11211,bind=127.0.0.1,fork,reuseaddr openssl:broken-shadow-990cz9og.dal0.kraft.cloud:11211 &
```

Then, run the following commands to test that it works (you should see output when incrementing):

```console
telnet 127.0.0.1 11211
set test 0 0 1
0
incr test 1
incr test 1
```

To exit telnet and stop the socat process, run:

```console
Ctrl + ]
Ctrl + C
kill -9 <PID>
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
