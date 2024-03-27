# Grafana

[Grafana](https://grafana.com) is the open source analytics & monitoring solution for every database.

To run Grafana on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 1024 .
```

After deploying, you can query the service using the provided URL.

## Learn more

- [Grafana's Documentation](https://grafana.com/docs/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
