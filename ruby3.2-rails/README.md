# Ruby3.2 Rails

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, invoke:

```console
kraft cloud deploy -M 1024 -p 443:3000 -e GEM_HOME=/usr/local/bundle -e BUNDLE_APP_CONFIG=/usr/local/bundle .
```

Then query the `/hello` path from the provided URL.

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
