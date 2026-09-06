FROM scratch
COPY --from=python:3.12-slim /usr/local/bin/python3 /usr/bin/python3
COPY --from=python:3.12-slim /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=python:3.12-slim /lib /lib
COPY --from=python:3.12-slim /usr/lib /usr/lib
COPY server.py /app/server.py
CMD ["/usr/bin/python3", "/app/server.py"]