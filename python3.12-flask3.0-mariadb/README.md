# Flask with MariaDB

[Flask](https://flask.palletsprojects.com/en/3.0.x/) is a micro web framework written in Python.

To run Tyk on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
This example uses a MariaDB back-end.
Clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud compose up
```

After deploying, you can query the service using the provided URL.

```console
curl https://<NAME>.<METRO>.kraft.host/hello
```
```text
{"data":[[6]]}
```

## Learn more

- [Flask's Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
