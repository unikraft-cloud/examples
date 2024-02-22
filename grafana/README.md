# Grafana

This examples demonstrates how to use [Grafana](https://grafana.com), the open source analytics & monitoring solution for every database.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 443:3000 -M 1024 .
```

Get the results of the deployment by visiting the webpage or using `curl`:

```console
curl  https://green-leaf-29gzos5s.dal0.kraft.cloud/login
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
