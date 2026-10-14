FROM perl:5.42.0-bookworm AS build

RUN set -xe ; \
    cpanm HTTP::Daemon


FROM gcr.io/distroless/cc-debian12:nonroot

# Perl binary
COPY --from=build /usr/local/bin/perl /usr/bin/perl

# Perl libraries
COPY --from=build /usr/local/lib/perl5 /usr/local/lib/perl5

# System libraries
COPY --from=build /usr/local/lib/perl5/5.42.0/x86_64-linux-gnu/CORE/libperl.so /usr/local/lib/perl5/5.42.0/x86_64-linux-gnu/CORE/libperl.so
COPY --from=build /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1

# Simple Perl HTTP server
COPY ./server.pl /usr/src/server.pl
