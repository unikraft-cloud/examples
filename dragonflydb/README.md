# DragonflyDB

[DragonflyDB](https://www.dragonflydb.io/) is a simple, performant, and cost-efficient in-memory data store.

To run DragonflyDB on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:6379 -M 512 .
```

After deploying, you can use `redis-cli` to query the service using the provided URL.

## Learn more

- [DragonflyDBS's Documentation](https://www.dragonflydb.io/docs)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
