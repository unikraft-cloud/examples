FROM --platform=linux/x86_64 mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /src

RUN dotnet new console
RUN rm Program.cs
COPY ./SimpleHttpServer.cs .
RUN dotnet build .

FROM scratch

# Binary executable
COPY --from=build /src/bin/Debug/net8.0 /usr/bin/app

# .NET libraries and confis
COPY --from=build /usr/share/dotnet/shared/Microsoft.NETCore.App/8.0.4 /usr/share/dotnet/shared/Microsoft.NETCore.App/8.0.4
COPY --from=build /usr/share/dotnet/host /usr/share/dotnet/host

# System libraries
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libicuuc.so.72 /lib/x86_64-linux-gnu/libicuuc.so.72
COPY --from=build /lib/x86_64-linux-gnu/libicudata.so.72 /lib/x86_64-linux-gnu/libicudata.so.72
COPY --from=build /lib/x86_64-linux-gnu/libicui18n.so.72 /lib/x86_64-linux-gnu/libicui18n.so.72
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
