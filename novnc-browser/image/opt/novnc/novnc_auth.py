"""websockify authentication plugin for HTTP Basic Auth from a file.

The plugin reads "<user>:<password>" from the file in --auth-source. Thus, the
password does not show in the command line of the processes.
"""

import hmac

from websockify.auth_plugins import BasicHTTPAuth


class FileBasicAuth(BasicHTTPAuth):
    def __init__(self, src=None):
        with open(src, "rb") as f:
            self.creds = f.read().rstrip(b"\n")
        super().__init__(src=None)

    def validate_creds(self, username, password):
        given = f"{username}:{password}".encode("latin-1")
        return hmac.compare_digest(given, self.creds)
