# Rust Rocket v0.5

[Rocket](https://rocket.rs/) is web framework for Rust that makes it simple to write fast, type-safe, secure web applications.

To run Rocket on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will build and deploy the files under `src/`.

After deploying, you can query the service using the provided URL, followed by paths such as `hello/world`.
See more in the `src/main.rs` source code file.

## Learn more

- [Rockets's Documentation](https://api.rocket.rs/v0.5/rocket/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
