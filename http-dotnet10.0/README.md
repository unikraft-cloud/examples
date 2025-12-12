# .NET on Unikraft Cloud

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

To deploy this application on Unikraft Cloud, invoke:

```console
kraft cloud deploy -p 443:8080 -M 512 .
```

## Learn more

- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
