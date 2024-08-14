# WASM (Wazero) on Go

This example is derived from [Wazero's "import go" example](https://github.com/tetratelabs/wazero/tree/main/examples/import-go) and shows how to define, import and call a wasm blob from Go and run it on Unikraft Cloud.
In the example, if the current year is 2024, and we give the argument 2000, [age-calculator.go](age-calculator.go) should output 24.

To run Wazero on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 . /age-calculator 2000
```

After deploying, you can query the service using the provided URL.

## Learn more

- [Wazero's Documentation](https://wazero.io/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
