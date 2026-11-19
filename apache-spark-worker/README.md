# Apache Spark Worker

[Apache Spark](https://spark.apache.org) is a unified engine for large-scala data analytics.

To run Hugo on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 2048 .
```

The command will start an instance of an Apache Spark worker.
This will not work until an Apaches Spark master is presented.

## Learn more

- [Apache Spark's Documentation](https://spark.apache.org/docs/latest/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
