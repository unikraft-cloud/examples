## Spin HTTP Example in C++

This example is derived from [Spin's `spin-http-cpp` example](https://github.com/fermyon/spin/tree/v2.1.0/examples/http-cpp) and shows how to run a simple example of a [Spin HTTP trigger](https://spin.fermyon.dev/http-trigger) implemented in C++ on KraftCloud.

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Then, clone this repository and `cd` into this directory.
To deploy this application on KraftCloud, simply invoke:

```
kraft cloud deploy -p 443:3000 -M 1024 .
```

You can test the trigger using e.g.:

```bash
curl -i https://young-cloud-cxf9szvi.fra0.kraft.cloud/hello
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
