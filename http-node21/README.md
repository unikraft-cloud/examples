# Node21

[Node,js](https://nodejs.org) is a free, open-source, cross-platform JavaScript runtime environment.

To run Node.js on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 256 .
```

The command will deploy the `server.js` file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Node.js's Documentation](https://nodejs.org/docs/latest/api/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
