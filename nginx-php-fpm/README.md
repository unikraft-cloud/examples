# NGINX and PHP FPM

[PHP FPM (FastCGI Process Manager)](https://www.php.net/manual/en/install.fpm.php) is a primary PHP FastCGI implementation containing some features (mostly) useful for heavy-loaded sites.

To run PHP FPM, a web server frontend is required, such as [NGINX](https://www.nginx.com/).

To run NGINX and PHP FPM on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).
Then clone this examples repository.
You will create two KraftCloud instances:

1. To create the PHP FPM instance, `cd` into the `php-fpm/` directory and run:

   ```console
   kraft cloud deploy --name php-fpm -p 9000:9000/tls -M 1024 .
   ```

   Be sure to use the `php-fpm` as the instance name.
   It is used by the NGINX configuration.

1. To create the NGINX frontend instance, `cd` into the `nginx/` directory and run:

   ```console
   kraft cloud deploy --name nginx-uk -p 443:8080 -M 756 .
   ```

After deploying, you can query the service using the provided URL.
Two queries can be made:

1. Test the NGINX frontend with a pure HTML query:

   ```
   curl https://<NAME>.<METRO>.kraft.host/hello.html
   ```

1. Test the NGINX + PHP FPM service with a PHP query:

   ```
   curl https://<NAME>.<METRO>.kraft.host/hello.php
   ```

The reply is an simple HTML "Hello, World!" web page.

## Learn more

- [PHP FPM's Documentation](https://www.php.net/manual/en/install.fpm.php)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
