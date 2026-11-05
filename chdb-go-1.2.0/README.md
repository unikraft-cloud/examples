# CHDB Go 1.21 Program.

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, simply invoke:

```console
kraft cloud deploy -M 1024 -p 443:8080 .
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
