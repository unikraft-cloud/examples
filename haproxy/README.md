# HAProxy

This example demonstrates how to use [HAProxy](https://www.haproxy.org), a free and open source software that provides a high availability load balancer and reverse proxy for TCP and HTTP-based applications that spreads requests across multiple servers.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 443:8404 -M 256 .
```

Get the results of the deployment by running or visiting the website:

```console
curl  https://green-leaf-29gzos5s.dal0.kraft.cloud/stats
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
