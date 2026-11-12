FROM python:3.12-bookworm AS build

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends libev-dev pax-utils

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY manage.py main.py /app/
COPY helloworld /app/helloworld/

RUN set -xe; \
    python3 manage.py collectstatic --noinput; \
    python3 manage.py migrate; \
    DJANGO_SUPERUSER_PASSWORD=unikraft python3 manage.py createsuperuser --noinput --username unikraft --email mail@example.com

RUN set -xe; \
    mkdir -p /rootfs/tmp; \
    /usr/bin/python3 /usr/bin/lddtree --copy-to-tree /rootfs /usr/local/bin/python3; \
    find /usr/local/lib/python3.12 -type f ! -name '_tkinter*' -print0 | xargs -0 /usr/bin/python3 /usr/bin/lddtree --skip-non-elfs --copy-to-tree /rootfs; \
    tar -C / -cf /tmp/data.tar etc/ld.so.cache usr/local/lib/python3.12 app; \
    tar -C /rootfs -xf /tmp/data.tar; \
    find /rootfs -type d -exec chmod 755 {} +; \
    chmod 1777 /rootfs/tmp; \
    chroot /rootfs /usr/local/bin/python3 -c 'import ctypes, glob; [ctypes.CDLL(f) for f in glob.glob("/usr/local/lib/python3.12/**/*.so", recursive=True) if "/_tkinter" not in f]'; \
    chroot /rootfs /usr/local/bin/python3 /app/manage.py check

FROM scratch

COPY --from=build /rootfs /
