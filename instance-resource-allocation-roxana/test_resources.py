#!/usr/bin/env python3

import socket
import sys
import urllib.error
import urllib.request

DEFAULT_TIMEOUT_S = 10


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        with urllib.request.urlopen(url, timeout=DEFAULT_TIMEOUT_S) as response:
            body = response.read().decode("utf-8")
    except (urllib.error.URLError, socket.timeout) as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(body)

    if "Hello from Unikraft Cloud!" not in body:
        print("Unexpected response", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
