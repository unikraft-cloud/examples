FROM python:3.11-slim-trixie AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./server.py /src/server.py

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    /usr/bin/python3 /usr/bin/lddtree --copy-to-tree /rootfs /usr/local/bin/python3; \
    find /usr/local/lib/python3.11 -type f ! -name '_tkinter*' -print0 | xargs -0 /usr/bin/python3 /usr/bin/lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar etc/ld.so.cache usr/local/lib/python3.11 src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/python3 -c 'import ctypes, glob, src.server; [ctypes.CDLL(f) for f in glob.glob("/usr/local/lib/python3.11/**/*.so", recursive=True) if "/_tkinter" not in f]'

FROM scratch

COPY --from=build /rootfs /
