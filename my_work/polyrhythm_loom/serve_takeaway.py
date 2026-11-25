#!/usr/bin/env python3
"""Serve the loom page and keep each finished round for a phone on the same Wi-Fi.

The QR code points at http://<this-mac>:8770/takeaway/<id>/
Images and video stay in my_work/_local/takeaway/, which git ignores.
"""
import json
import os
import re
import socket
import sys
import uuid
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORE = ROOT.parent / "_local" / "takeaway"
STORE.mkdir(parents=True, exist_ok=True)
PORT = 8770
MAX_BODY = 80 * 1024 * 1024

PAGE = """<!doctype html>
<html lang="zh">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weaving With · 这一轮</title>
<style>
body{{margin:0;padding:20px;background:#0B0D11;color:#ECE6D6;font:16px/1.45 "Noto Sans SC",sans-serif}}
h1{{font-size:28px;margin:0 0 4px}}
p{{color:#8B909C}}
img,video{{width:100%;height:auto;display:block;background:#000;margin:12px 0}}
a{{color:#ECE6D6}}
</style>
<h1>Weaving With</h1>
<p>这一轮的复节奏。长按图片可以保存。视频是这一轮的过程。</p>
<p>This round. Hold the picture to save it. The video is the round itself.</p>
<img src="cloth.png" alt="这一轮的布">
{video}
<p><a href="cloth.png" download>保存图片</a> · <a href="round.webm" download>保存视频</a></p>
"""

VIDEO = '<video src="round.webm" controls playsinline></video>'


def lan_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def read_parts(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0 or length > MAX_BODY:
        return {}
    ctype = handler.headers.get("Content-Type", "")
    mark = "boundary="
    if mark not in ctype:
        return {}
    boundary = ctype.split(mark, 1)[1].split(";", 1)[0].strip().strip('"').encode()
    body = handler.rfile.read(length)
    parts = {}
    for chunk in body.split(b"--" + boundary):
        if b"Content-Disposition" not in chunk:
            continue
        head, _, data = chunk.partition(b"\r\n\r\n")
        if data.endswith(b"\r\n"):
            data = data[:-2]
        name = b""
        for bit in head.split(b";"):
            bit = bit.strip()
            if bit.startswith(b"name="):
                name = bit.split(b"=", 1)[1].strip(b'"')
        if name:
            parts[name.decode()] = data
    return parts


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/host":
            body = json.dumps({"ip": lan_ip(), "port": PORT}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        take = re.fullmatch(r"/takeaway/([0-9a-f]+)/?", path)
        if take:
            folder = STORE / take.group(1)
            page = folder / "index.html"
            if not page.is_file():
                self.send_error(404)
                return
            data = page.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        file_match = re.fullmatch(r"/takeaway/([0-9a-f]+)/(cloth\.png|round\.webm)", path)
        if file_match:
            target = STORE / file_match.group(1) / file_match.group(2)
            if not target.is_file():
                self.send_error(404)
                return
            kind = "image/png" if target.suffix == ".png" else "video/webm"
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/takeaway":
            self.send_error(404)
            return
        parts = read_parts(self)
        image = parts.get("image")
        if not image or not image.startswith(b"\x89PNG"):
            self.send_error(400, "need a png")
            return
        ident = uuid.uuid4().hex[:10]
        folder = STORE / ident
        folder.mkdir(parents=True, exist_ok=False)
        (folder / "cloth.png").write_bytes(image)
        video = parts.get("video") or b""
        has_video = len(video) > 32
        if has_video:
            (folder / "round.webm").write_bytes(video)
        html = PAGE.format(video=VIDEO if has_video else "")
        (folder / "index.html").write_text(html, encoding="utf-8")
        body = json.dumps({"id": ident}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve_https(port=8443):
    import ssl
    import subprocess
    cert_dir = ROOT.parent / "_local" / "loom_cert"
    cert_dir.mkdir(parents=True, exist_ok=True)
    cert, key = cert_dir / "cert.pem", cert_dir / "key.pem"
    ip = lan_ip()
    subprocess.check_call([
        "openssl", "req", "-x509", "-newkey", "rsa:2048", "-sha256", "-days", "60", "-nodes",
        "-keyout", str(key), "-out", str(cert),
        "-subj", "/CN=loom",
        "-addext", f"subjectAltName=IP:{ip},IP:127.0.0.1,DNS:localhost",
    ])
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    print(f"tablet https://{ip}:{port}/tablet.html", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    os.chdir(ROOT)
    if "--https" in sys.argv:
        serve_https()
    else:
        server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
        print(f"loom http://{lan_ip()}:{PORT}/camera.html", flush=True)
        server.serve_forever()
