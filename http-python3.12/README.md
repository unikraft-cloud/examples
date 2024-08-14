# Simple Python 3.12 HTTP Server

This is a simple HTTP server written in the [Python](https://www.python.org/) programming language.

To run this example on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 512 .
```

The command will build the `server.py` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Python's Documentation](https://www.python.org/doc/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
