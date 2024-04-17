# Go 1.21 with Redis deployed with a `Composefile` on KraftCloud

This is a simple HTTP server written in the [Go](https://go.dev/) programming language and uses Redis via the [Go redis module](github.com/redis/go-redis) to share keys and their values.
The project can be instantiated using the accompanying `Composefile`.

To run this example on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```
kraft cloud compose up
```

Then, retrieve the domain which has been provisioned with:

```
kraft cloud service ls -o list
```

Find the FQDN.

To set a value in Redis via the Go server, invoke:

```
curl -X POST -d "key=my-key" -d "value=my-value" https://<FQDN>
```

You can then retrieve the value by accessing the path:

```
curl https://<FQDN>/\?key\=my-key
```

## Learn more

- [Go's Documentation](https://go.dev/doc/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
