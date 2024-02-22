# Hugo Server

This example demonstrates how to use [Hugo](https://gohugo.io/commands/hugo_server/), a high performance webserver, with the [ananke](https://github.com/budparr/gohugo-theme-ananke.git) theme.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 443:1313 -M 512 .
```

Fetch the URL from the output and open it in your browser or use `curl`:

```console
curl https://falling-silence-wb7fv6nr.dal0.kraft.cloud
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
