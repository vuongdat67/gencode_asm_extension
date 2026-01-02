from model import CodeBert_Seq2Seq
from utils import set_seed

set_seed(42)

m = CodeBert_Seq2Seq(
    ip_path="fg-codebert",
    raw_path="fg-codebert",
    decoder_layers=6,
    fix_encoder=False,
    beam_size=5,
    max_source_length=64,
    max_target_length=64,
    load_model_path="model/python/checkpoint-best-rouge/pytorch_model.bin",
    layer_attention=True,
    l2_norm=True,
    fusion=True
)

source = "add value x to variable total"
similarity = "add var0 to var1"

preds = m.predict(source, similarity)

print("Best:", preds[0])
print("Others:", preds[1:])
