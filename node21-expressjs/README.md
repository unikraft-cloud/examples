# Node 21 Express

[Express](https://expressjs.com/) is a fast, unopinionated, minimalist web framework for Node.js.

To run Express on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 256 .
```

The command will deploy the files under `app/`.

After deploying, you can query the service using the provided URL.

## Learn more

- [Express's Documentation](https://expressjs.com/en/5x/api.html)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
