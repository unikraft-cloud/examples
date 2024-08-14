# Node 21 SvelteKit

[SvelteKit](https://kit.svelte.dev/) is built on Svelte, a UI framework that uses a compiler to let you write breathtakingly concise components that do minimal work in the browser.

This project was generated using [`npm create svelte@latest`](https://kit.svelte.dev/docs/creating-a-project), uses the [`@sveltejs/adapter-node`](https://kit.svelte.dev/docs/adapter-node) adapter and includes a `Kraftfile` and `Dockerfile` to run on Unikraft Cloud.

To run SvelteKit on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -p 443:3000 -M 256 .
```

The command will deploy the files in the current directory.

After deploying, you can query the service using the provided URL.

## Learn more

- [SvelteKit's Documentation](https://kit.svelte.dev/docs/introduction)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
