# NGINX

[NGINX](https://www.nginx.com/) is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.

To run NGINX on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

The command will deploy the files under `rootfs/`.

After deploying, you can query the service using the provided URL.

## Learn more

- [NGINX's Documentation](https://nginx.org/en/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
