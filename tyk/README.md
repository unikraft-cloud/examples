# Tyk

[Tyk](https://tyk.io/) is an API gateway and management platform.

To run Tyk on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and do the steps below.
Tyk uses Redis as the backend for storing its information.

1. Create a service group for the Redis and Tyk instance:

   ```console
   kraft cloud service create --name tyk-network 443:8080/http+tls
   ```

1. Create a Redis instance:

   ```console
   kraft cloud inst create --start --name tyk-redis -g tyk-network redis:7.2
   ```

1. Create a Tyk instance:

   ```console
   kraft cloud deploy -g tyk-network .
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
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
