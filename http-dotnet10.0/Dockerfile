FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0 AS build
ARG TARGETARCH
ARG BUILDPLATFORM

WORKDIR /src
RUN dotnet new console
RUN rm Program.cs
COPY ./SimpleHttpServer.cs .
RUN dotnet publish -a "$TARGETARCH" --self-contained -o /app

FROM --platform=$TARGETPLATFORM mcr.microsoft.com/dotnet/sdk:10.0 AS runtime

FROM scratch

# Binary executable
COPY --from=build /app /app

# System libraries
COPY --from=runtime /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=runtime /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=runtime /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=runtime /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=runtime /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=runtime /lib/x86_64-linux-gnu/libicuuc.so.74 /lib/x86_64-linux-gnu/libicuuc.so.74
COPY --from=runtime /lib/x86_64-linux-gnu/libicudata.so.74 /lib/x86_64-linux-gnu/libicudata.so.74
COPY --from=runtime /lib/x86_64-linux-gnu/libicui18n.so.74 /lib/x86_64-linux-gnu/libicui18n.so.74
COPY --from=runtime /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
