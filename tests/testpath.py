import torch
from model import CodeBert_Seq2Seq
from utils.assembly import raw_to_ip, clean_nl

def demo_with_parser():
    print("="*80)
    print("ExploitGen Demo with Template Parser")
    print("="*80)
    
    # Load model
    print("\nLoading model...")
    model = CodeBert_Seq2Seq(
        ip_path='./fg-codebert',
        raw_path='./fg-codebert',
        decoder_layers=6,
        fix_encoder=False,
        beam_size=10,
        max_source_length=64,
        max_target_length=64,
        load_model_path='./model/assembly/checkpoint-best-rouge/pytorch_model.bin',
        layer_attention=True,
        l2_norm=True,
        fusion=True
    )
    print("Model loaded!\n")
    
    # Test cases
    test_cases = [
        "decrease the counter and jump to decode if not zero else jump short to shellcode",
        "not operation of current byte in esi",
        "add 0x10 to the current byte in esi",
        "move the value 0x0b into register eax"
    ]
    
    for i, raw_nl in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"[Test {i}]")
        print(f"{'='*80}")
        print(f"Raw NL: {raw_nl}")
        
        # Use Template Parser to get template
        try:
            # Parse NL to template (without code)
            cleaned_nl = clean_nl(raw_nl)
            # For demo, we manually create template
            # In production, you'd use the full parser
            
            # Generate code
            results = model.predict(
                source=raw_nl,
                similarity=raw_nl  # Simplified: use raw as template
            )
            
            print(f"\nGenerated code:")
            print(f"  Best: {results[0]}")
            print(f"\n  Alternatives:")
            for j, code in enumerate(results[1:6], 2):
                print(f"    [{j}] {code}")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    demo_with_parser()