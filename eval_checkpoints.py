import os
from model import CodeBert_Seq2Seq
from utils import set_seed

# Eval 4 checkpoints: assembly, assembly2, python, python2
# Uses test sets in code-trained/exploitgen-data

TASKS = [
    {
        "name": "assembly1",
        "lang": "assembly",
        "ckpt": "model/assembly/checkpoint-best-rouge/pytorch_model.bin",
        "test_csv": "code-trained/exploitgen-data/assembly/test.csv",
    },
    {
        "name": "assembly2",
        "lang": "assembly",
        "ckpt": "model/assembly2/checkpoint-best-rouge/pytorch_model.bin",
        "test_csv": "code-trained/exploitgen-data/assembly/test.csv",
    },
    {
        "name": "python1",
        "lang": "python",
        "ckpt": "model/python/checkpoint-best-rouge/pytorch_model.bin",
        "test_csv": "code-trained/exploitgen-data/python/test.csv",
    },
    {
        "name": "python2",
        "lang": "python",
        "ckpt": "model/python2/checkpoint-best-rouge/pytorch_model.bin",
        "test_csv": "code-trained/exploitgen-data/python/test.csv",
    },
]


def eval_task(task):
    lang = task["lang"]
    ckpt = task["ckpt"]
    test_csv = task["test_csv"]
    out_dir = os.path.join("model", lang, f"test_results_{task['name']}")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 80)
    print(f"Eval {task['name']} | lang={lang} | ckpt={ckpt}")
    print(f"test_csv={test_csv}")
    print(f"out_dir={out_dir}")

    model = CodeBert_Seq2Seq(
        ip_path="fg-codebert",
        raw_path="fg-codebert",
        decoder_layers=6,
        fix_encoder=False,
        beam_size=10,
        max_source_length=64,
        max_target_length=64,
        load_model_path=ckpt,
        layer_attention=True,
        l2_norm=True,
        fusion=True,
    )

    metrics = model.test(
        test_filename=test_csv,
        test_batch_size=16,
        output_dir=out_dir,
    )

    print(f"Metrics: {metrics}")
    print(f"Saved to {out_dir}")


def main():
    set_seed(42)
    for task in TASKS:
        eval_task(task)


if __name__ == "__main__":
    main()
