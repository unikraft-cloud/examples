FROM python:3.11-slim-trixie AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends pax-utils

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --from=ghcr.io/astral-sh/uv:0.9.14 /uv /bin/
COPY tool-constraints.txt tool-constraints.txt
RUN uv tool install arxiv-mcp-server --constraints tool-constraints.txt

COPY ./server.py /src/server.py

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    /usr/bin/python3 /usr/bin/lddtree --copy-to-tree /rootfs /usr/local/bin/python; \
    find /usr/local/lib/python3.11 /root/.local -type f ! -name '_tkinter*' -print0 | xargs -0 /usr/bin/python3 /usr/bin/lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar etc/ld.so.cache root/.local usr/local/lib/python3.11 src; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/python -c 'import ctypes, glob, src.server; [ctypes.CDLL(f) for d in ("/usr/local/lib/python3.11", "/root/.local/share/uv/tools") for f in glob.glob(f"{d}/**/*.so", recursive=True) if "/_tkinter" not in f]'; \
    chroot /rootfs /root/.local/share/uv/tools/arxiv-mcp-server/bin/python -c 'import arxiv_mcp_server.server'

FROM scratch

COPY --from=build /rootfs /
