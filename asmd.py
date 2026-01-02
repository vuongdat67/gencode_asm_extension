import sys
import json
import argparse
from typing import Dict

from inference_asm import run_single, set_seed


def parse_var_map(raw: Dict[str, str]) -> Dict[str, str]:
    return {k: v for k, v in raw.items() if isinstance(v, str)}


def handle_request(req: Dict[str, object]):
    source = req.get("source", "")
    similarity = req.get("similarity", "")
    var_map = parse_var_map(req.get("var_map", {}) or {})
    best, stats = run_single(source, similarity, var_map)
    return {"best": best, **stats}


def serve(stdin, stdout):
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
        except Exception as e:
            res = {"error": str(e)}
        stdout.write(json.dumps(res, ensure_ascii=False) + "\n")
        stdout.flush()


def main():
    parser = argparse.ArgumentParser(description="ExploitGen ASM daemon (JSON over stdin/stdout)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    set_seed(args.seed)
    serve(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
