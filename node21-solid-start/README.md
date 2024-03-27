# Node 21 Solid Start

[Solid Start](https://start.solidjs.com/) a meta-framework that provides the platform to put all of web-related pieces together in a one location.

To run Solid Start on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 256 .
```

The command will deploy the files in the current directory.

After deploying, you can query the service using the provided URL.

## Learn more

- [Solid Starts's Documentation](https://start.solidjs.com/getting-started/what-is-solidstart)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
