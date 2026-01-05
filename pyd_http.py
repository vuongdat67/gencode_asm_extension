import json
import sys
import traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict

from inference_python import run_single, set_seed

HOST = "127.0.0.1"
PORT = 9138

# Ensure UTF-8 console to avoid Windows cp1252 issues
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: Dict):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):  # silence default logging
        return

    def do_POST(self):
        if self.path != "/infer":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("content-length", "0"))
            body = self.rfile.read(length)
            req = json.loads(body.decode("utf-8")) if body else {}
            source = req.get("source", "")
            similarity = req.get("similarity", "")
            if not source or not similarity:
                self._send(400, {"error": "source and similarity are required"})
                return
            print(f"[REQ] len={len(source)} source='{source[:120]}' sim='{similarity[:120]}'")
            best, stats = run_single(source, similarity, {})
            resp = {"best": best, **stats}
            self._send(200, resp)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            self._send(500, {"error": str(e)})


def main():
    set_seed(42)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving ExploitGen Python HTTP on http://{HOST}:{PORT}/infer")
    server.serve_forever()


if __name__ == "__main__":
    main()
