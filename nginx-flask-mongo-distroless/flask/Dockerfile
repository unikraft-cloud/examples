FROM python:3.12-bookworm AS builder

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app


FROM gcr.io/distroless/cc-debian12

WORKDIR /app

COPY --from=builder /usr/local/bin/python3.12 /usr/local/bin/python3.12

COPY --from=builder /usr/local/lib/libpython3.12.so.1.0 /usr/local/lib/libpython3.12.so.1.0

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12

COPY --from=builder /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1

COPY --from=builder /app /app
