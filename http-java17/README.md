# Simple Java 17 HTTP Server

This is a simple HTTP server written in the [Java](https://www.java.com/en/) programming language.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```
kraft cloud deploy --metro fra0 -p 443:8080 -M 512 .
```

The command will build and deploy the `SimpleHTTPServer.java` source code file.

After deploying, you can query the service using the provided URL.

## Learn more

- [Java's Documentation](https://docs.oracle.com/en/java/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
