# Redis

[Redis](https://redis.io) is an open-source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

To run Redis on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 6379:6379/tls -M 512 .
```

First, open a connection to the Redis server (save the pid):

```console
socat tcp-listen:6379,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.host:6379 &
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

- [Redis's Documentation](https://redis.io/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
