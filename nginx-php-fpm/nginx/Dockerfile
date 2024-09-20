FROM nginx:1.25.3-bookworm AS build

# Custom configuration files, including using a single process for Nginx
COPY ./etc/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./etc/nginx/fastcgi_params /etc/nginx/fastcgi_params

# Web root
COPY ./var/www/html/hello.html ./var/www/html/hello.html

RUN rm /var/log/nginx/error.log
RUN rm /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log
RUN touch /var/log/nginx/access.log
