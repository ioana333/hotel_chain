from __future__ import annotations

import http.server
import json
import socketserver
import urllib.error
import urllib.request
from pathlib import Path

HOST = "127.0.0.1"
PORT = 5500
GATEWAY = "http://127.0.0.1:8000"
ROOT = Path(__file__).resolve().parent


class BrowserAppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self.proxy()
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self.proxy()
            return
        self.send_error(404)

    def do_PUT(self):
        if self.path.startswith("/api/"):
            self.proxy()
            return
        self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/api/"):
            self.proxy()
            return
        self.send_error(404)

    def proxy(self):
        target = GATEWAY + self.path.removeprefix("/api")
        body = None
        if "Content-Length" in self.headers:
            body = self.rfile.read(int(self.headers["Content-Length"]))
        request = urllib.request.Request(
            target,
            data=body,
            method=self.command,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
                self.end_headers()
                self.wfile.write(payload)
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", exc.headers.get("Content-Type", "application/json"))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as exc:
            payload = json.dumps({"detail": f"API Gateway unavailable: {exc}"}).encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(payload)


if __name__ == "__main__":
    with socketserver.ThreadingTCPServer((HOST, PORT), BrowserAppHandler) as server:
        print(f"Browser app: http://{HOST}:{PORT}")
        print(f"Proxy target: {GATEWAY}")
        server.serve_forever()
