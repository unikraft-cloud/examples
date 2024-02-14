# Llama2 inference

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, simply invoke:

```
kraft cloud deploy -M 1024 -p 443:8080 .
```

Note that in this example we assign 1G of memory. The amount required
will vary depending on the model.

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
