# Node 21 NextJS

[NextJS](https://nextjs.org/) enables you to create high-quality web applications with the power of React components.

To run NextJS on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 256 .
```

The command will build the files in the current directory.

After deploying, you can query the service using the provided URL.

## Learn more

- [NextJS's Documentation](https://nextjs.org/docs)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
