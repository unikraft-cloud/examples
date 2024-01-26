# Traefik on KraftCloud

[Traefik](https://traefik.io/traefik/) is the leading open-source reverse proxy and load balancer for HTTP and TCP-based applications.


To run Traefik on KraftCloud, clone this examples repository and `cd` into this directory, then invoke:

```console
kraft cloud deploy -M 256 -p 443:2015 .
```

## Learn more

- [Caddy's Documentation](https://caddyserver.com/docs/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)

