FROM --platform=$BUILDPLATFORM nginx:1.29.0-alpine

COPY ./nginx.conf /etc/nginx/nginx.conf.template
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
