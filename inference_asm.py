import re
from model import CodeBert_Seq2Seq
from utils import set_seed

# exploitgen-asm-v1 defaults
USE_KEYSTONE = True
NORMALIZE_OUTPUT = True
MODEL_CACHE = {}
try:
    from keystone import Ks, KS_ARCH_X86, KS_MODE_32
    HAS_KEYSTONE = True
except ImportError:
    HAS_KEYSTONE = False


def load_model(ckpt_path: str, beam_size: int = 10) -> CodeBert_Seq2Seq:
    # Load một model với checkpoint cho assembly
    if ckpt_path in MODEL_CACHE:
        return MODEL_CACHE[ckpt_path]
    _model = CodeBert_Seq2Seq(
        ip_path="fg-codebert",
        raw_path="fg-codebert",
        decoder_layers=6,
        fix_encoder=False,
        beam_size=beam_size,
        max_source_length=64,
        max_target_length=64,
        load_model_path=ckpt_path,
        layer_attention=True,
        l2_norm=True,
        fusion=True,
    )
    MODEL_CACHE[ckpt_path] = _model
    return _model


def bracket_ok(s: str) -> bool:
    return s.count("[") == s.count("]") and s.count("[") <= 2


def asm_grammar_filter(candidates: list[str]) -> list[str]:
    """Lọc nhanh về cú pháp cơ bản + normalize spacing."""
    filtered = []
    for c in candidates:
        s = c.strip().lower()
        s = s.replace(" ,", ",").replace(", ", ", ")
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r"\s*,\s*", " , ", s)
        s = s.replace("[ ", "[").replace(" ]", "]")
        s = re.sub(r"\s*\]\s*", "]", s)
        s = re.sub(r"\s*\[\s*", "[", s)

        # Yêu cầu tối thiểu: opcode + 1-2 operands
        if not re.match(r"^[a-z][a-z0-9]{1,8}\s+[^\s]+(\s*,\s*[^\s]+)?$", s):
            continue
        if not re.match(r"^[a-z0-9_\[\],+\-x ]+$", s):
            continue
        if not bracket_ok(s):
            continue
        # Loại placeholder chung chung
        if '[var]' in s:
            continue
        filtered.append(s)
    return filtered


def asm_semantic_score(code: str) -> int:
    """Ưu tiên register thật, immediate hex, và symbol buffer."""
    score = 0
    for reg in ("esi", "eax", "ebx", "ecx", "edx", "rsi", "rax", "rbx", "rcx", "rdx"):
        if reg in code:
            score += 2
            break
    if '0x' in code:
        score += 2
    if re.search(r",\s*0x0\b", code):
        score -= 5  # phạt immediate 0
    for sym in ("buff", "buf", "data", "ptr"):
        if sym in code:
            score += 1
            break
    return score


def normalize_syntax(code: str) -> str:
    """Chuẩn hoá khoảng trắng/dấu phẩy/ngoặc cho dễ đọc và stable."""
    s = code.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*,\s*", ", ", s)
    s = s.replace("[ ", "[").replace(" ]", "]")
    s = re.sub(r"\s*\[\s*", "[", s)
    s = re.sub(r"\s*\]\s*", "]", s)
    # Thêm khoảng trắng sau opcode nếu thiếu
    s = re.sub(r"^(\w+)(\[)", r"\1 [", s)
    # Đảm bảo có khoảng giữa opcode và toán hạng
    s = re.sub(r"^(\w+)\s*(\S)", r"\1 \2", s)
    return s


def keystone_check(code: str) -> bool:
    """Optional: assemble to ensure strict syntax. Skips if placeholders present."""
    if not USE_KEYSTONE or not HAS_KEYSTONE:
        return True
    if re.search(r"var\d", code):
        return True  # placeholders would fail keystone nếu chưa resolve
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        ks.asm(code)
        return True
    except Exception:
        return False


def resolve_vars(code: str, var_map: dict[str, str] | None) -> str:
    """Thay placeholder var\d bằng giá trị cụ thể (immediate/register/symbol)."""
    if not var_map:
        return code
    out = code
    for k, v in var_map.items():
        out = re.sub(rf"\b{k}\b", v, out)
    return out


def keystone_rank(candidates: list[str], var_map: dict[str, str] | None) -> list[str]:
    """Re-rank bằng Keystone sau khi resolve placeholder.

    - Nếu có var_map: resolve rồi keystone check trên bản đã resolve.
    - Nếu không có var_map: giữ nguyên; chỉ xếp theo semantic score.
    """
    scored = []
    for c in candidates:
        resolved = resolve_vars(c, var_map)
        normed = normalize_syntax(resolved) if NORMALIZE_OUTPUT else resolved
        k_ok = keystone_check(normed)
        score = asm_semantic_score(normed)
        if not immediate_matches_var(normed, var_map):
            score -= 10
        score += semantic_bonus(normed, var_map)
        scored.append((k_ok, score, normed, c))
    scored.sort(reverse=True)
    return [orig for _, _, _, orig in scored]


def keystone_pass_rate(candidates: list[str], var_map: dict[str, str] | None) -> float | None:
    if not USE_KEYSTONE or not HAS_KEYSTONE:
        return None
    total = 0
    ok = 0
    for c in candidates:
        resolved = resolve_vars(c, var_map)
        normed = normalize_syntax(resolved) if NORMALIZE_OUTPUT else resolved
        if re.search(r"var\d", normed):
            continue  # chưa resolve đủ để check
        total += 1
        if keystone_check(normed):
            ok += 1
    if total == 0:
        return None
    return ok / total


def immediate_matches_var(code: str, var_map: dict[str, str] | None) -> bool:
    """Đảm bảo literal hex trong code khớp var_map nếu có."""
    if not var_map:
        return True
    for _, v in var_map.items():
        if v.startswith("0x") and v not in code:
            return False
    return True


def semantic_bonus(code: str, var_map: dict[str, str] | None) -> int:
    """Thưởng nếu dest là memory của var1 và imm khớp var0."""
    if not var_map:
        return 0
    bonus = 0
    dest = re.match(r"\s*add\s+([^,]+)", code)
    if dest:
        d = dest.group(1)
        if '[' in d and ']' in d:
            for k, v in var_map.items():
                if k == 'var1' and v in d:
                    bonus += 5
        else:
            # Nếu dest là register mà src là memory, phạt nhẹ
            src_mem = re.search(r",\s*[^,]*\[", code)
            if src_mem:
                bonus -= 3
    # Thưởng nhỏ nếu immediate khớp var0
    for k, v in var_map.items():
        if k == 'var0' and v in code:
            bonus += 2
    return bonus


def dedup_preserve(seq):
    seen = set()
    out = []
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def ensemble_predict(source: str, similarity: str, var_map: dict[str, str] | None = None) -> tuple[str, list[str], dict]:
    ckpts = [
        "model/assembly/checkpoint-best-rouge/pytorch_model.bin",
        "model/assembly2/checkpoint-best-rouge/pytorch_model.bin",
    ]

    beams = []
    for ck in ckpts:
        m = load_model(ck)
        preds = m.predict(source, similarity)
        beams.extend(preds)

    beams = dedup_preserve(beams)
    filtered = asm_grammar_filter(beams)
    # Keystone filter sau khi resolve nếu có var_map
    keeplist = []
    for c in filtered:
        resolved = resolve_vars(c, var_map)
        if keystone_check(resolved):
            keeplist.append(c)

    ranked = keystone_rank(keeplist, var_map) if keeplist else beams

    if ranked:
        best = ranked[0]
        others = ranked[1:]
    else:
        best, others = "", []

    # Resolve + normalize cho output
    def postproc(code: str) -> str:
        resolved = resolve_vars(code, var_map)
        return normalize_syntax(resolved) if NORMALIZE_OUTPUT else resolved

    best_out = postproc(best) if best else ""
    others_out = [postproc(o) for o in others]

    stats = {
        "keystone_pass_rate": keystone_pass_rate(keeplist, var_map),
        "candidates": len(keeplist),
    }
    return best_out, others_out, stats


def run_single(source: str, similarity: str, var_map: dict[str, str]) -> tuple[str, dict]:
    """Wrapper cho CLI/REST: trả về best và stats."""
    best, others, stats = ensemble_predict(source, similarity, var_map=var_map)
    stats["others"] = others
    return best, stats


def run_csv(input_csv: str, output_csv: str, var_map_fn) -> None:
    """Chạy batch: input_csv phải có cột raw_nl, temp_nl.

    var_map_fn: callable nhận row (dict/pandas Series) và trả về dict var_map.
    Ghi output_csv với cột best và các trường stats JSON.
    """
    import pandas as pd
    rows = pd.read_csv(input_csv)
    out_best = []
    out_stats = []
    for _, row in rows.iterrows():
        source = row.get("raw_nl", "")
        similarity = row.get("temp_nl", "")
        var_map = var_map_fn(row)
        best, stats = run_single(source, similarity, var_map)
        out_best.append(best)
        out_stats.append(stats)
    rows["best"] = out_best
    rows["stats"] = out_stats
    rows.to_csv(output_csv, index=False)


if __name__ == "__main__":
    set_seed(42)

    source = "add 0x10 to the current byte in esi"
    similarity = "add var0 to current byte in var1"
    var_map = {
        "var0": "0x10",
        "var1": "esi",
    }

    best, others, stats = ensemble_predict(source, similarity, var_map=var_map)
    print("Best:", best)
    print("Others:", others)
    print("Stats:", stats)
