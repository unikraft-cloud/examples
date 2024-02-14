# Nginx on KraftCloud

[Nginx](https://nginxr.com/) is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache

To run Nginx on KraftCloud, clone this examples repository and `cd` into this directory, then invoke:

```console
kraft cloud deploy -p 443:8080 .
```

The command will build and deploy the files under the `rootfs/` directory.
Feel free to modify and redeploy!

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)

