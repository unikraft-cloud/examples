# Caddy on KraftCloud

[Caddy](https://caddyserver.com/) is a powerful, enterprise-ready, open source web server with automatic HTTPS written in Go.


To run Caddy on KraftCloud, clone this examples repository and `cd` into this directory, then invoke:

```console
kraft cloud deploy -p 443:2015 .
```

The command will build and deploy the files under `rootfs`. Feel free to modify and redeploy!

## Learn more

- [Caddy's Documentation](https://caddyserver.com/docs/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)

