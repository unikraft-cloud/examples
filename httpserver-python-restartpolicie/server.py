import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/":
            self._respond(200, "Hello from restart-demo!\n")

        elif parsed.path == "/health":
            self._respond(200, "OK\n")

        elif parsed.path == "/exit":
            try:
                code = int(params.get("code", ["0"])[0])
            except ValueError:
                self._respond(400, "Invalid exit code\n")
                return


                self._respond(400, "Invalid exit code\n")

                return

            self._respond(200, f"Exiting with code {code}...\n")
            self.wfile.flush()
            sys.exit(code)
        else:
            self._respond(404, "Not found\n")

    def _respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        print(f"[LOG] {self.address_string()} - {format % args}", flush=True)

if __name__ == "__main__":
    print(f"Server open on port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()