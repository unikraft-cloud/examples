FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-noble AS build

ARG TARGETARCH

WORKDIR /src
RUN dotnet new console
RUN rm Program.cs
COPY ./SimpleHttpServer.cs .
RUN dotnet publish -a "$TARGETARCH" --self-contained -o /app

FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-noble AS runtime

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

COPY --from=build /app /app

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    find /app -type f -print0 | xargs -0 lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    lddtree --copy-to-tree /rootfs /lib/*/libicuuc.so.?? /lib/*/libicui18n.so.??; \
    tar -C / -cf /tmp/data.tar app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp

FROM scratch

COPY --from=runtime /rootfs /
