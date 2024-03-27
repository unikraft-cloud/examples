# Python Django

[Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

To run Django on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository and `cd` into this directory, and invoke:

```console
kraft cloud deploy -M 512 -p 443:80 .
```

The command will deploy files in the current directory.

After deploying, you can query the service using the provided URL.

## Important notes

The example sets `ALLOWED_HOSTS` to `*` and runs in debug mode.
For a production site read the deployment guides of the Django project carefully.

## Learn more

- [Django's Documentation](https://docs.djangoproject.com/en/5.0/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
