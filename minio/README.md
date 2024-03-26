# MinIO

[MinIO](https://min.io/) is a High-Performance Object Storage system.

To run MinIO on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:9001/http+tls -p 9000:9000/tls -M 512 .
```

After deploying, you can query the service using the provided URL.

## Learn more

- [MinIO's Documentation](https://min.io/docs/minio/kubernetes/upstream/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
