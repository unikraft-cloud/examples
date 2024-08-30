FROM python:3.12-bookworm AS build

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

FROM scratch

COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.8 /lib/x86_64-linux-gnu/libffi.so.8
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /app /app
