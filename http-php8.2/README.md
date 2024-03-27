# Simple PHP8.2 HTTP Server

This is a simple HTTP server written in the [PHP](https://www.php.net/) programming language.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 -M 256 .
```

The command will deploy the `server.php` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [PHP's Documentation](https://www.php.net/docs.php)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
