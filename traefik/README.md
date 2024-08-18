# Traefik on Unikraft Cloud

[Traefik](https://traefik.io/traefik/) is the leading open-source reverse proxy and load balancer for HTTP and TCP-based applications.

To run Traefik on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 512 -p 443:80/tls+http -p 8080:8080/tls .
```

The command will deploy the `default.toml` configuration file.

Important security note: this exposes the dashboard on port 8080 *without* authentication.

After deploying, you can query the service using the provided URL.
Use the `/dashboard` path for the URL.

## Learn more

- [Traefik's Documentation](https://doc.traefik.io/traefik/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
