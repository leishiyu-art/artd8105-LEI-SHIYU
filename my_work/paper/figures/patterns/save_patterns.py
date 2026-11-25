#!/usr/bin/env python3
"""Receives pattern PNGs posted by the loom page."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        name = self.path.split("?", 1)[0].lstrip("/")
        if not name.endswith(".png") or ".." in name:
            self.send_error(400)
            return
        length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(length)
        dest = ROOT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        body = str(dest.stat().st_size).encode()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(f"saved {dest.name} {len(data)}", flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8799), Handler).serve_forever()
