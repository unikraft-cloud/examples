#!/usr/bin/env python3
"""noVNC web server and WebSocket proxy to x11vnc, with authentication.

Usage: novnc_server.py <port> [<auth file>]

The auth file contains "<user>:<password>". If it is given, each HTTP request
and each WebSocket request must have one of these credentials:

- The header "Authorization: Basic <base64 of user:password>".
- The query parameter "token=<password>".
- The session cookie, which a browser gets when it opens a page with a
  correct token.

Pages of other sites can show the desktop in a frame, with a token in the URL
of the frame. The session cookie is partitioned: a browser sends it only while
the top-level page is on the site where the browser got the cookie. A response
to other credentials cannot show in a frame of another site. A browser sends
its stored
credentials also for a WebSocket that a page of another site starts. Thus, a
WebSocket request with an Origin of another host or port gets 403, and a
WebSocket request with only the cookie must have the Origin of the desktop.

A browser that opens a page with a correct token gets a redirect to the same
URL without the token, thus the password does not stay in the address bar. A
request without correct credentials gets 401, and the browser shows a login
dialog. The log never shows the token.
"""

import base64
import binascii
import hmac
import logging
import multiprocessing
import re
import secrets
import sys
from urllib.parse import unquote_plus, urlsplit, urlunsplit

from websockify import websocketproxy
from websockify.auth_plugins import AuthenticationError

WEB = "/opt/noVNC"
TARGET_HOST = "127.0.0.1"
TARGET_PORT = 5900
# Other hosts cannot set a cookie with the __Host- prefix
COOKIE = "__Host-novnc_session"
TOKEN = "token"
# websockify uses TLS only if this file exists, as its command line does
CERT = "self.pem"
TOKEN_VALUE = re.compile(rf"({TOKEN}=).*?(?=&| HTTP/|$)")


def is_token(piece):
    # Only the literal name, which the log filter also finds
    return piece.partition("=")[0] == TOKEN


def default_port(scheme):
    return {"https": 443, "http": 80}.get(scheme)


def without_token(path):
    """Return @path without the token, other parameters stay as they are."""
    parts = urlsplit(path)
    query = "&".join(p for p in parts.query.split("&")
                     if p and not is_token(p))
    return urlunsplit(("", "", parts.path, query, parts.fragment))


class Handler(websocketproxy.ProxyRequestHandler):
    def basic_ok(self):
        scheme, _, value = self.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "basic":
            return False
        try:
            given = base64.b64decode(value.strip(" "), validate=True)
        except (binascii.Error, ValueError):
            return False
        return hmac.compare_digest(given, self.server.creds)

    def token_ok(self):
        pieces = [p for p in urlsplit(self.path).query.split("&")
                  if is_token(p)]
        if len(pieces) != 1:
            return False
        token = unquote_plus(pieces[0].partition("=")[2])
        return hmac.compare_digest(token.encode(), self.server.password)

    def session_ok(self):
        # A request can have more than one cookie with this name
        ok = False
        cookies = ";".join(self.headers.get_all("Cookie", []))
        for part in cookies.split(";"):
            name, sep, value = part.strip().partition("=")
            if sep and name == COOKIE:
                ok |= hmac.compare_digest(value.encode(),
                                          self.server.session.encode())
        return ok

    def same_origin(self):
        try:
            origin = urlsplit(self.headers.get("Origin", ""))
            host = urlsplit("//" + self.headers.get("Host", ""))
            if origin.hostname is None or origin.hostname != host.hostname:
                return False
            origin_port = origin.port or default_port(origin.scheme)
            host_port = host.port
        except ValueError:
            return False

        # Behind the TLS proxy of the platform, Host has no port
        if host_port is None:
            return origin.scheme == "https" and origin_port == 443
        return origin_port == host_port

    def is_navigation(self):
        mode = self.headers.get("Sec-Fetch-Mode")
        if mode is not None:
            return mode == "navigate"
        return "text/html" in self.headers.get("Accept", "")

    def log_message(self, format, *args):
        super().log_message("%s", TOKEN_VALUE.sub(r"\1<hidden>",
                                                  format % args))

    def frame_ok(self):
        # A request that failed before its headers has no path or headers
        if self.server.creds is None or not hasattr(self, "headers"):
            return False
        return self.token_ok() or self.session_ok()

    def end_headers(self):
        # Only the token and the partitioned cookie allow frames of other sites
        if not self.frame_ok():
            self.send_header("Content-Security-Policy",
                             "frame-ancestors 'self'")
            self.send_header("X-Frame-Options", "SAMEORIGIN")
        super().end_headers()

    def reject(self, code, headers):
        ex = AuthenticationError(response_code=code, response_headers=headers)
        self.send_auth_error(ex)
        raise ex

    def auth_connection(self):
        if self.server.creds is None:
            return

        upgrade = self.headers.get("Upgrade", "").lower() == "websocket"
        strong = self.basic_ok() or self.token_ok()
        if not strong and not self.session_ok():
            self.reject(401, {"WWW-Authenticate": 'Basic realm="noVNC"'})
        if upgrade and not self.same_origin() and \
                ("Origin" in self.headers or not strong):
            self.reject(403, {})

        # websockify writes the path to the log
        self.path = without_token(self.path)

    def do_GET(self):
        # Exchange a correct token for the session cookie
        if self.server.creds is not None and self.is_navigation() and \
                self.token_ok():
            # Only a path, so that the browser stays on this host
            location = "/" + without_token(self.path).lstrip("/\\")
            self.send_response(302)
            self.send_header("Location", location)
            self.send_header("Set-Cookie",
                             f"{COOKIE}={self.server.session}; Path=/; "
                             "Secure; HttpOnly; SameSite=None; Partitioned")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        super().do_GET()


def main():
    # Each connection runs in a child process, which must inherit the setup
    multiprocessing.set_start_method("fork")

    port = int(sys.argv[1])
    creds = None
    if len(sys.argv) > 2 and sys.argv[2]:
        with open(sys.argv[2], "rb") as f:
            creds = f.read().rstrip(b"\n")

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    server = websocketproxy.WebSocketProxy(
        RequestHandlerClass=Handler, listen_port=port,
        target_host=TARGET_HOST, target_port=TARGET_PORT,
        web=WEB, web_auth=creds is not None, cert=CERT,
        ssl_options=websocketproxy.select_ssl_version("default"))

    server.creds = creds
    server.password = creds.split(b":", 1)[1] if creds is not None else None
    server.session = secrets.token_urlsafe(32)
    server.start_server()


if __name__ == "__main__":
    main()
