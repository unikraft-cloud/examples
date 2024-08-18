# Python Flask

[Flask](https://flask.palletsprojects.com/en/3.0.x/) is a micro web framework written in Python.

To run Flask on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 512 -p 443:8080 .
```

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL.

## Learn more

- [Flask's Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
