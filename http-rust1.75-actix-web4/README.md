# Rust Actix Web

[Actix Web](https://actix.rs/) is a powerful, pragmatic, and extremely fast web framework for Rust.

To run Actix Web on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will build and deploy the files under `src/`.

After deploying, you can query the service using the provided URL.

## Learn more

- [Actix's Documentation](https://actix.rs/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
