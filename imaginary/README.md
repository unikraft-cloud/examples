# Imaginary

[Imaginary](https://github.com/h2non/imaginary) is a fast, simple, scalable, Docker-ready HTTP microservice for high-level image processing.

To run Imaginary on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 256 .
```

After deploying, you can query the service using the provided URL.

## Learn more

- [Imaginary's Documentation](https://fly.io/docs/app-guides/run-a-global-image-service/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
