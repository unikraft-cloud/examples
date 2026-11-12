FROM python:3.12-alpine3.22 AS build

RUN apk add --no-cache lddtree

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    lddtree -l /usr/local/bin/python3 > /tmp/libs.txt; \
    find /usr/local/lib/python3.12 -type f ! -name '_tkinter*' -exec scanelf -BF '%F' {} + | tr '\n' '\0' | xargs -0 -r lddtree -l >> /tmp/libs.txt; \
    sort -u -o /tmp/libs.txt /tmp/libs.txt; \
    tar -cf /tmp/libs.tar -T /tmp/libs.txt; \
    tar -C /rootfs -xf /tmp/libs.tar; \
    tar -C / -cf /tmp/data.tar usr/local/lib/python3.12 app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/python3 -c 'import ctypes, glob, flask, pymongo; [ctypes.CDLL(f) for f in glob.glob("/usr/local/lib/python3.12/**/*.so", recursive=True) if "/_tkinter" not in f]'

FROM scratch

COPY --from=build /rootfs /
