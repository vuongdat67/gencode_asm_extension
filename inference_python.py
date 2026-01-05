import re
import sys
from model import CodeBert_Seq2Seq
from utils import set_seed

MODEL_CACHE = {}
NORMALIZE_OUTPUT = True

# Ensure UTF-8 stdout/stderr to avoid Windows cp1252 encode errors
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load_model(ckpt_path: str, beam_size: int = 10) -> CodeBert_Seq2Seq:
    if ckpt_path in MODEL_CACHE:
        return MODEL_CACHE[ckpt_path]
    _model = CodeBert_Seq2Seq(
        ip_path="fg-codebert",
        raw_path="fg-codebert",
        decoder_layers=6,
        fix_encoder=False,
        beam_size=beam_size,
        max_source_length=256,
        max_target_length=256,
        load_model_path=ckpt_path,
        layer_attention=True,
        l2_norm=True,
        fusion=True,
    )
    MODEL_CACHE[ckpt_path] = _model
    return _model


def normalize_code(code: str) -> str:
    text = code.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def dedup_preserve(seq):
    seen = set()
    out = []
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def predict_best(source: str, similarity: str) -> tuple[str, list[str], dict]:
    ckpts = [
        "model/python/checkpoint-best-rouge/pytorch_model.bin",
    ]

    beams = []
    for ck in ckpts:
        m = load_model(ck)
        preds = m.predict(source, similarity)
        beams.extend(preds)

    beams = [normalize_code(b) for b in beams]
    beams = [b for b in beams if b]
    beams = dedup_preserve(beams)

    if beams:
        best = beams[0]
        others = beams[1:]
    else:
        best, others = "", []

    stats = {
        "candidates": len(beams),
    }
    return best, others, stats


def run_single(source: str, similarity: str, var_map=None) -> tuple[str, dict]:
    # var_map is unused for python but kept for interface parity
    best, others, stats = predict_best(source, similarity)
    stats["others"] = others
    return best, stats


if __name__ == "__main__":
    set_seed(42)
    src = "sort list ascending"
    sim = "sort var0 ascending"
    best, stats = run_single(src, sim, {})
    print("Best:", best)
    print("Stats:", stats)
