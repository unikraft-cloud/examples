# Simple Go 1.21 HTTP Server

This is a simple HTTP server written in the [Go](https://go.dev/) programming language.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will build and deploy the `server.go` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Go's Documentation](https://go.dev/doc/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
