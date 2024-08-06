# Spin Wagi HTTP example

This example is derived from [Spin's `spin-wagi-http` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/spin-wagi-http) and shows how to run a Spin application serving routes from two programs written in different languages (Rust and C++) using both the Spin executor and the Wagi executor on KraftCloud.

To run Spin Wagi on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 1024 .
```

The command will build and deploy the files in the current directory.

After deploying, you can query the service using the provided URL.
Use the `/hello` and `/goodbye` paths for the URL.

## Learn more

- [Spin's Documentation](https://developer.fermyon.com/spin/v2/index)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
