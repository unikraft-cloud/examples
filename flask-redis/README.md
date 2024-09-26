# Compose: Flask and Redis

This is a [Compose](https://unikraft.cloud/docs/guides/features/compose/)-based example of [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [Redis](https://redis.io/).
It is imported from the [`awesome-compose` repository](https://github.com/docker/awesome-compose).

To run Flask and Redis with Compose on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL.
Find out the provided URL by using:

```console
kraft cloud instance list
```

## Learn more

- [The Compose Specification](https://github.com/compose-spec/compose-spec/blob/main/spec.md)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
