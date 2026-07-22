FROM --platform=linux/x86_64 oven/bun:alpine AS bun

FROM scratch

COPY --from=bun /usr/local/bin/bun /usr/bin/bun

COPY --from=bun /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=bun /usr/lib/libstdc++.so.6 /usr/lib/libstdc++.so.6
COPY --from=bun /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=bun /usr/lib/libgcc_s.so.1 /usr/lib/libgcc_s.so.1

COPY ./server.ts /usr/src/server.ts
