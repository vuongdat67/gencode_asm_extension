from model import CodeBert_Seq2Seq
from utils import set_seed

LANG = "python"  # hoặc "assembly"
BASE_MODEL = "fg-codebert"
CKPT = f"model/{LANG}/checkpoint-best-rouge/pytorch_model.bin"

set_seed(42)
m = CodeBert_Seq2Seq(
    ip_path=BASE_MODEL, raw_path=BASE_MODEL,
    decoder_layers=6, fix_encoder=False,
    beam_size=5, max_source_length=64, max_target_length=64,
    load_model_path=CKPT,
    layer_attention=True, l2_norm=True, fusion=True
)

source = "mô tả tự nhiên gốc..."
similarity = "mô tả template (temp_nl)..."
preds = m.predict(source, similarity)
print("Best:", preds[0])        # phương án tốt nhất
print("Alt beams:", preds[1:])  # các phương án khác