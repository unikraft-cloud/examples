from http.server import BaseHTTPRequestHandler, HTTPServer
import socket


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = (
            "Hello from Unikraft Cloud!\n"
            "This application demonstrates port mapping.\n"
            f"Served by: {socket.gethostname()}\n"
        )

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Listening on port 8080...")
    server.serve_forever()
