# Compose: Nginx and Golang

This is a [Compose](https://unikraft.cloud/docs/guides/features/compose/)-based example of a [Go]() HTTP server and an [Nginx](https://nginx.org/en/) proxy.
It is imported from the [`awesome-compose` repository](https://github.com/docker/awesome-compose).

To run Nginx and Golang with Compose on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL for Nginx.
Golang is only running in the backend with a public URL.
Find out the Nginx provided URL by using:

```console
kraft cloud instance list
```

## Learn more

- [The Compose Specification](https://github.com/compose-spec/compose-spec/blob/main/spec.md)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
