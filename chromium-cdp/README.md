# Run Chromium (with CDP) on Unikraft Cloud

Run Chromium as a browser server, exposing a [CDP (Chrome DevTools Protocol)](https://chromedevtools.github.io/devtools-protocol/) websocket interface.
To run Chromium on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy -M 4096 -p 443:8080 .
```

The command will deploy the files in the current directory.
It results in the creation of a remote web-based browser service.

To query the service you need to use a CDP client.
You can use the Python-based implementation in the `test/` directory.

## Learn more

- [CDP Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
