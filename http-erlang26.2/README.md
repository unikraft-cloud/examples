# Simple Erlang HTTP Server

This is a simple HTTP server written in the Erlang programming language.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 512 .
```

The command will build and deploy the `http_server.erl` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Erlang's Documentation](https://www.erlang.org/doc/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
