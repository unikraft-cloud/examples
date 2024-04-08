# Wordpress

[Wordpress](https://wordpress.com/) is a web content management system.

To run Wordpress on KraftCloud, first [install the `kraft` CLI tool](https://unikraft.org/docs/cli).

Wordpress requires connecting three KraftCloud instances:

* A MariaDB database instance
* A Wordress instance, using PHP FPM (*FastCGI Process Manager*)
* An Nginx web server

## Set Up MariadB

To set up MariaDB, enter the `mariadb/` example directory.
Create a MariaDB instance and assign it the `mariadb` name:

```console
kraft cloud deploy --metro fra0 --name mariadb -p 3306:3306/tls -M 1024 mariadb:latest
```

The MariaDB instance can be referenced by other KraftCloud instances as `mariadb.internal`.

After deploying, you can query the service using the provided URL.
For that, first use `socat` to open a TLS connection to port `3306` (MariaDB's listening port):

```console
socat tcp-listen:3306,bind=127.0.0.1,fork,reuseaddr openssl:<NAME>.<METRO>.kraft.cloud:3306 &
```

Create the Wordpress database, user and password on MariaDB.
Log in with the `root` user and the `unikraft` password:

```console
$ mysql -h 127.0.0.1 -u root -punikraft
```

And now run these commands to create the `wordpress` database, and the `wordpress` user with the `wordpresspass` password:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
[...]
MariaDB [(none)]> create database wordpress;
Query OK, 1 row affected (0.031 sec)

MariaDB [(none)]> grant all privileges on wordpress.* to 'wordpress'@'%' identified by 'wordpresspass';
```

## Set Up Wordpress

To set up Wordpress, enter this (`wordpress/`) example directory.
Create a Wordpress instance by providing the environment variables for the MariaDB hostname, the database, the username and the passport.
Assign it the `wordpress` name:

```
kraft cloud deploy -e WORDPRESS_DB_HOST="mariadb.internal" -e WORDPRESS_DB_NAME="wordpress" -e WORDPRESS_DB_USER="wordpress" -e WORDPRESS_DB_PASSWORD="wordpresspass" --name wordpress -M 1024 .
```

This will create a Wordress instance using PHP FPM (*FastCGI Process Manager*).
We use the `mariadb.internal` name to connect to the MariaDB instance started above.
The Wordpress instance can be referenced by other KraftCloud instances as `wordpress.internal`.

## Set Up Nginx

To access Wordpress, a web server is required as a FastCGI proxy.
We use Nginx.

To set up Nginx, enter the `nginx/` example directory.
Update the Nginx configuration to use the FastCGI connection.
That is, in the `rootfs/` directory of the `nginx/` example, create two files: `/etc/nginx/nginx.conf` and `/etc/nginx/fastcgi_params`.

The contents of the `rootfs/etc/nginx/fastcgi_params` file should be:

```text
fastcgi_param   QUERY_STRING            $query_string;
fastcgi_param   REQUEST_METHOD          $request_method;
fastcgi_param   CONTENT_TYPE            $content_type;
fastcgi_param   CONTENT_LENGTH          $content_length;

fastcgi_param   SCRIPT_FILENAME         $document_root$fastcgi_script_name;
fastcgi_param   SCRIPT_NAME             $fastcgi_script_name;
fastcgi_param   PATH_INFO               $fastcgi_path_info;
fastcgi_param   PATH_TRANSLATED         $document_root$fastcgi_path_info;
fastcgi_param   REQUEST_URI             $request_uri;
fastcgi_param   DOCUMENT_URI            $document_uri;
fastcgi_param   DOCUMENT_ROOT           $document_root;
fastcgi_param   SERVER_PROTOCOL         $server_protocol;

fastcgi_param   GATEWAY_INTERFACE       CGI/1.1;
fastcgi_param   SERVER_SOFTWARE         nginx/$nginx_version;

fastcgi_param   REMOTE_ADDR             $remote_addr;
fastcgi_param   REMOTE_PORT             $remote_port;
fastcgi_param   SERVER_ADDR             $server_addr;
fastcgi_param   SERVER_PORT             $server_port;
fastcgi_param   SERVER_NAME             $server_name;

fastcgi_param   HTTPS                   $https;

# PHP only, required if PHP was built with --enable-force-cgi-redirect
fastcgi_param   REDIRECT_STATUS         200;
```

The contents of the `rootfs/etc/nginx/nginx.conf` file should be:

```text
worker_processes  1;
daemon            off;
master_process    off;
user root root;

events {
  worker_connections  64;
}

http {
  include mime.types;
  default_type application/octet-stream;

  open_file_cache           max=10000 inactive=30s;
  open_file_cache_min_uses  2;
  open_file_cache_errors    on;

  error_log stderr error;
  access_log off;

  keepalive_timeout     10s;
  keepalive_requests    10000;
  send_timeout          10s;

  server {
    listen              8080;
    server_name         localhost;
    root                /wwwroot;
    index               index.php index.html;

    location ~ [^/]\.php(/|$) {
      fastcgi_split_path_info ^(.+?\.php)(/.*)$;
      if (!-f $document_root$fastcgi_script_name) {
          return 404;
      }

      # Mitigate https://httpoxy.org/ vulnerabilities
      fastcgi_param HTTP_PROXY "";

      fastcgi_pass wordpress-weq53.internal:9000;
      fastcgi_index index.php;

      # include the fastcgi_param setting
      include /etc/nginx/fastcgi_params;

      # SCRIPT_FILENAME parameter is used for PHP FPM determining
      #  the script name. If it is not set in fastcgi_params file,
      # i.e. /etc/nginx/fastcgi_params or in the parent contexts,
      # please comment off following line:
      # fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
    }
  }
}
```

Now create an Nginx instance:

```console
kraft cloud deploy --metro fra0 -p 443:8080 .
```

After deploying, you can query the service using the provided URL.
It will show you an install screen for Wordpress.

## Learn more

- [Wordpress's Documentation](https://wordpress.org/documentation/)
- [KraftCloud's Documentation](https://docs.kraft.cloud)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)
