FROM --platform=linux/x86_64 lscr.io/linuxserver/code-server:4.103.2 AS code-server

FROM --platform=linux/x86_64 ubuntu:latest

COPY --from=code-server /app /app
