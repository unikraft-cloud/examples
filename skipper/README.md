# Skipper on KraftCloud

[Skipper](https://opensource.zalando.com/skipper/) is an HTTP router and reverse proxy for service composition.

To run Skipper on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:9090 .
```

The command will deploy the `example.eskip` configuration file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Skipper's Documentation](https://opensource.zalando.com/skipper/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
