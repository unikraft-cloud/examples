# Hugo

[Hugo](https://gohugo.io/) is one of the most popular open-source static site generators.

To run Hugo on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:1313 -M 512 .
```

The command will deploy the files under `site/`.

After deploying, you can query the service using the provided URL.

## Learn more

- [Hugo's Documentation](https://gohugo.io/documentation/).
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
