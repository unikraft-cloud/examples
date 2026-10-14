# Tyk

[Tyk](https://tyk.io/) is an API gateway and management platform.

To run Tyk on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

After deploying, you can query the service using the provided URL.
Use the `/hello` path after the URL, such as below:

```console
curl https://<NAME>.<METRO>.kraft.host/hello
```
```text
{"status":"pass","version":"v5.3.0-dev","description":"Tyk GW","details":{"redis":{"status":"pass","componentType":"datastore","time":"2024-04-30T10:37:29Z"}}}
```

## Learn more

- [Tyk's Documentation](https://tyk.io/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
