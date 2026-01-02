import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict

from inference_asm import run_single, set_seed

HOST = "127.0.0.1"
PORT = 9137


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
            var_map = req.get("var_map", {}) or {}
            if not source or not similarity:
                self._send(400, {"error": "source and similarity are required"})
                return
            best, stats = run_single(source, similarity, var_map)
            resp = {"best": best, **stats}
            self._send(200, resp)
        except Exception as e:  # noqa: BLE001
            self._send(500, {"error": str(e)})


def main():
    set_seed(42)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving ExploitGen ASM HTTP on http://{HOST}:{PORT}/infer")
    server.serve_forever()


if __name__ == "__main__":
    main()
