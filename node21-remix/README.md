# Node 21 Remix Example

This example uses the [Remix](https://remix.run/).
To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, invoke:

```console
kraft cloud deploy -p 443:3000 -M 512 .
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)