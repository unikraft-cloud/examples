# WAMR (iwasm)

This example is done by running [WAMR](https://github.com/bytecodealliance/wasm-micro-runtime) in KraftCloud.

```console
kraft cloud deploy .
```

Then access the logs via `kraft cloud instance logs` and you should see:
```
Hello, World!
```

This currently fails because of an Unikraft error, and the actual message is:
```
Failed to init stack guard pages
Init runtime environment failed.
```

## Learn more

- [KraftCloud's Documentation](https://docs.kraft.cloud)
