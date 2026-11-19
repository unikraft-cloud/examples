# Restate

[Restate](ihttps://restate.dev/) is the simplest way to write resilient workflows, event-driven applications, and async tasks.

To run Restate on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and create a volume and then a Restate instance:

```console
kraft cloud volume create --metro fra0 --name restate --size 1024
kraft cloud deploy --metro fra0 -p 443:8080 -M 512 -v restate:/var/lib/restate
```

The command will deploy Restate using the configuration file `conf.yml`.

After deploying, you can query the service using the provided URL.

## Learn more

- [Restate's Documentation](https://docs.restate.dev/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
