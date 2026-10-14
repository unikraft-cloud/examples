#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (
            "Hello from Unikraft Cloud!\n"
            "This instance was started with explicit resource allocation.\n"
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


def main():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on port 8080")
    server.serve_forever()


if __name__ == "__main__":
    main()
