# Llama2.c Inference

[Llama2.c](https://github.com/karpathy/llama2.c) is Llama2 inference in one file of pure C.

To run LLama2.c on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 1024 -p 443:8080 .
```

The command will build and deploy the files under `rootfs/`.
Note that in this example we assign 1G of memory.
The amount required will vary depending on the model.

After deploying, you can query the service using the provided URL.

## Learn more

- [Llama2.c's Documentation](https://github.com/karpathy/llama2.c/blob/master/README.md)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
