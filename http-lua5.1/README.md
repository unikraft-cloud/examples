# Simple Lua 5.1.5 HTTP Server

This is a simple HTTP server written in the [Lua](https://www.lua.org/) programming language.

To run this example on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will deploy the `http_server.lua` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Lua's Documentation](https://www.lua.org/docs.html)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
