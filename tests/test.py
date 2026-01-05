from model import CodeBert_Seq2Seq
from utils import set_seed

LANG = "assembly"  # hoặc "python"
BASE_MODEL = "fg-codebert"                     # model nền để load config/tokenizer
BEST_CKPT = f"model/{LANG}/checkpoint-best-rouge/pytorch_model.bin"
TEST_CSV = f"code-trained/exploitgen-data/{LANG}/test.csv"
OUT_DIR = f"model/{LANG}/test_results_new"

set_seed(42)
model = CodeBert_Seq2Seq(
    ip_path=BASE_MODEL, raw_path=BASE_MODEL,
    decoder_layers=6, fix_encoder=False,
    beam_size=10, max_source_length=64, max_target_length=64,
    load_model_path=BEST_CKPT,
    layer_attention=True, l2_norm=True, fusion=True
)

model.test(test_filename=TEST_CSV, test_batch_size=16, output_dir=OUT_DIR)
print("Đã ghi kết quả vào", OUT_DIR)