# C++ Boost

[Boost](https://www.boost.org/doc/) is a set of libraries for the C++ programming language.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will build and deploy the `http_server.cpp` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Boost's Documentation](https://www.boost.org/doc/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
