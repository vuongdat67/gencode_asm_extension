import argparse
import json
import subprocess
import sys
from typing import Dict

from inference_asm import run_single, set_seed


def parse_var_map(var_args) -> Dict[str, str]:
    """Parse --var var0=0x10 --var var1=esi into dict."""
    var_map: Dict[str, str] = {}
    if var_args:
        for item in var_args:
            if "=" not in item:
                raise ValueError(f"Invalid --var format: {item}. Use var0=0x10")
            k, v = item.split("=", 1)
            var_map[k.strip()] = v.strip()
    return var_map


def main():
    parser = argparse.ArgumentParser(description="ExploitGen ASM CLI (late-fusion ensemble)")
    parser.add_argument("--source", required=False, default="", help="Raw NL input (raw_nl)")
    parser.add_argument("--similarity", required=False, default="", help="Template NL input (temp_nl)")
    parser.add_argument(
        "--var",
        action="append",
        default=[],
        help="Variable mapping varX=value (immediate/register/symbol). Example: --var var0=0x10 --var var1=esi",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--server", action="store_true", help="Run as JSON daemon (stdin/stdout)")
    parser.add_argument("--client", action="store_true", help="Emit one JSON request for piping to daemon")

    args = parser.parse_args()
    set_seed(args.seed)
    var_map = parse_var_map(args.var)

    if args.server:
        from asmd import serve
        serve(sys.stdin, sys.stdout)
        return

    if args.client:
        req = json.dumps({"source": args.source, "similarity": args.similarity, "var_map": var_map})
        print(req)
        return

    # Direct mode requires inputs
    if not args.source or not args.similarity:
        parser.error("--source and --similarity are required in direct mode (non --server/--client)")

    best, stats = run_single(args.source, args.similarity, var_map)

    if args.json:
        print(json.dumps({"best": best, **stats}, ensure_ascii=False, indent=2))
    else:
        print("Best:", best)
        print("Stats:", stats)


if __name__ == "__main__":
    main()
