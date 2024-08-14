# Wordpress

[Wordpress](https://wordpress.com/) is a web content management system.

To run Wordpress on Unikraft Cloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

This Wordpress builds connects together three types of services:

* A MariaDB database
* A Wordress setup, using PHP FPM (*FastCGI Process Manager*)
* An Nginx web server

Deploy the instance using:

```console
kraft cloud deploy --metro fra0 -p 443:80 -M 4096 .
```

After deploying, you can query the service using the provided URL.
It will show you an install screen for Wordpress.

## Learn more

- [Wordpress's Documentation](https://wordpress.org/documentation/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
