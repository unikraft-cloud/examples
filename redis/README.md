# Redis

This examples demonstrates how to use [Redis](https://redis.io), an open-source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 6379:6379/tls -M 512 .
```

First, open a connection to the Redis server (save the pid):

```console
socat tcp-listen:6379,bind=127.0.0.1,fork,reuseaddr openssl:dark-night-g652ndeb.dal0.kraft.cloud:6379 &
```

Then use `redis-cli` or `redis-benchmark` to test the connection (keep in mind that `socat` will also slow down your benchmark):

```console
redis-benchmark -t ping,set,get -n 10000
```

Stop the connection with the PID of the `socat` process, e.g.:

```console
kill -9 <PID>
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
