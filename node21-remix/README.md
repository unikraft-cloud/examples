# Node 21 Remix

[Remix](https://remix.run/)  is a full stack web framework that lets you focus on the user interface and work back through web standards to deliver a fast, slick, and resilient user experience.

To run Remix on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 512 .
```

The command will deploy the files in the current directory.

After deploying, you can query the service using the provided URL.

## Learn more

- [Remix's Documentation](https://remix.run/docs/en/main)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
