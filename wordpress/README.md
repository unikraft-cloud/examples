# Wordpress

[Wordpress](https://wordpress.com/) is a web content management system.

To run Wordpress on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Wordpress requires connecting two KraftCloud instances:

* A MariaDB database instance
* A Wordress instance, using PHP FPM (*FastCGI Process Manager*) and Nginx

## Set Up MariadB

To set up MariaDB, enter the `mariadb/` subdirectory.
Create a MariaDB instance and assign it the `mariadb` name:

```console
kraft cloud deploy --metro fra0 --name mariadb-wordpress -M 1024 .
```

The MariaDB instance can be referenced by other KraftCloud instances as `mariadb-wordpress.internal`.

## Set Up Wordpress

To set up Wordpress, be sure to be part of this directory.
Create a Wordpress instance by providing the environment variables for the MariaDB hostname, the database, the username and the passport.
Assign it the `wordpress` name:

```console
kraft cloud deploy -e WORDPRESS_DB_HOST="mariadb-wordpress.internal" -e WORDPRESS_DB_NAME="wordpress" -e WORDPRESS_DB_USER="wordpress" -e WORDPRESS_DB_PASSWORD="wordpresspass" --name wordpress -M 1024 -p 443:8080 .
```

This will create a Wordress instance using PHP FPM (*FastCGI Process Manager*) and Nginx as the front-end / poxy.
We use the `mariadb-wordpress.internal` name to connect to the MariaDB instance started above.

After deploying, you can query the service using the provided URL.
It will show you an install screen for Wordpress.
Proceed with the install process to have your Wordpress installation.

## Learn more

- [Wordpress's Documentation](https://wordpress.org/documentation/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
