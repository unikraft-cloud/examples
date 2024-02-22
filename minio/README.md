# MinIO

This examples demonstrates how to use [MinIO](https://min.io), a High Performance Object Storage which is Open Source, Amazon S3 compatible, Kubernetes Native and is designed for cloud native workloads like AI.

To get started, simply clone this repository and `cd` into this directory.
Then, run:

```console
kraft cloud deploy -p 443:9001/http+tls -p 9000:9000/tls -M 512 .
```

Get the results of the deployment by running the following command or visiting the website:

```console
curl https://spring-wood-6qlhc4ck.dal0.kraft.cloud
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
