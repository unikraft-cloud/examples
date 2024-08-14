# Bun

[Bun](https://bun.sh/) is an all-in-one toolkit for JavaScript and TypeScript apps.

To run Bun on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 512 .
```

After deploying, you can query the service using the provided URL.

## Learn more

- [Bun's Documentation](https://bun.sh/docs)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
