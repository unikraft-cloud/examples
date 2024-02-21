# Tokio (Rust) Example

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Start by cloning this repository and `cd` into this directory.
To deploy this application on KraftCloud, invoke:

```console
kraft cloud deploy -p 443:8080 .
```

Then try using curl on the resulting URL.

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
