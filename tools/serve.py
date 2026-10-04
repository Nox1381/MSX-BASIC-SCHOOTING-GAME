#!/usr/bin/env python3
"""Serve the browser launcher locally; WebMSX is loaded from its official host."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--host", default="127.0.0.1")
args = parser.parse_args()
directory = Path(__file__).resolve().parents[1] / "docs"
handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
server = ThreadingHTTPServer((args.host, args.port), handler)
print(f"Play at http://{args.host}:{args.port}/", flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
