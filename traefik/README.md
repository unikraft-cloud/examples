# Traefik on KraftCloud

[Traefik](https://traefik.io/traefik/) is the leading open-source reverse proxy and load balancer for HTTP and TCP-based applications.


To run Traefik on KraftCloud, clone this examples repository and `cd` into this directory, then invoke:

```console
kraft cloud deploy -M 512 -p 443:80/tls+http -p 8080:8080/tls .
```

Important security note: this exposes the dashboard on port 8080 *without* authentication.

To check for output you can use `curl`, or a browser:

```console
curl https://holy-cherry-rye39b1x.dal0.kraft.cloud:8080/dashboard
```

## Learn more

- [Caddy's Documentation](https://caddyserver.com/docs/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)

