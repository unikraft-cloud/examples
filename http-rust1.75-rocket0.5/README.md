# Rocket v0.5 (Rust) Example

To run this example, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

This example was derived from [Rocket's "hello" example](https://github.com/rwf2/Rocket/tree/v0.5/examples/hello).

Start by cloning this repository and `cd` into this directory.
To deploy this application on KraftCloud, invoke:

```
kraft cloud deploy -p 443:8080 .
```

Then try visiting one of the available paths:
- https://<NAME>.<METRO>.kraft.cloud/hello/world
- https://<NAME>.<METRO>.kraft.cloud/hello/мир
- https://<NAME>.<METRO>.kraft.cloud/wave/Rocketeer/100
- https://<NAME>.<METRO>.kraft.cloud/?emoji
- https://<NAME>.<METRO>.kraft.cloud/?name=Rocketeer
- https://<NAME>.<METRO>.kraft.cloud/?lang=ру
- https://<NAME>.<METRO>.kraft.cloud/?lang=ру&emoji
- https://<NAME>.<METRO>.kraft.cloud/?emoji&lang=en
- https://<NAME>.<METRO>.kraft.cloud/?name=Rocketeer&lang=en
- https://<NAME>.<METRO>.kraft.cloud/?emoji&name=Rocketeer
- https://<NAME>.<METRO>.kraft.cloud/?name=Rocketeer&lang=en&emoji
- https://<NAME>.<METRO>.kraft.cloud/?lang=ru&emoji&name=Rocketeer

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [How to build `Dockerfile` root filesystems with BuildKit](https://unikraft.org/docs/getting-started/integrations/buildkit)
