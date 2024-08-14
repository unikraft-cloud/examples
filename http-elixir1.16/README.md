# Simple Elixir HTTP Server

This is a simple HTTP server written in the Elixir programming language.
The initial contents of this example were created by using the command:

```console
mix new --app server . --sup
```

To run this example on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 1024 .
```

The command will build and deploy the implementation in `lib/`.
After deploying, you can query the service using the provided URL.

## Learn more

- [Elixir's Documentation](https://elixir-lang.org/docs.html)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
