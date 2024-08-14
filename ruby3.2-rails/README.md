# Ruby3.2 Rails

[Rails](https://rubyonrails.org/) is a server-side web application framework written in Ruby.

To run Rails on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy --metro fra0 -M 1024 -p 443:3000 -e GEM_HOME=/usr/local/bundle -e BUNDLE_APP_CONFIG=/usr/local/bundle .
```

The command will build and deploy the files under `rootfs/`.

After deploying, you can query the service using the provided URL.
Use the `/hello` path for the provided URL.

## Learn more

- [Rails's Documentation](https://guides.rubyonrails.org/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
