## ExploitGen ASM v1 – Hướng dẫn nhanh

### Tổng quan
Ensemble 2 checkpoint assembly (late-fusion), lọc cú pháp, keystone optional, ràng buộc var_map. Cung cấp CLI trực tiếp và daemon stdin/stdout.

### Chuẩn bị
- Python env đã cài deps của dự án (torch, transformers, keystone-engine nếu muốn USE_KEYSTONE=True).
- Checkpoints: `model/assembly/checkpoint-best-rouge/pytorch_model.bin` và `model/assembly2/checkpoint-best-rouge/pytorch_model.bin`.
- Model base: thư mục `fg-codebert` có tokenizer/config.

### CLI trực tiếp
```
python asm_cli.py `
	--source "add 0x10 to the current byte in esi" `
	--similarity "add var0 to current byte in var1" `
	--var var0=0x10 --var var1=esi `
	--json
```
Kết quả: best + stats (others trong stats).

### Daemon (stdin/stdout JSON)
Chạy daemon (load model 1 lần, cache trong process):
```
python asmd.py
```
Gửi request (mỗi dòng 1 JSON), ví dụ PowerShell:
```
echo '{"source":"add 0x10 to the current byte in esi","similarity":"add var0 to current byte in var1","var_map":{"var0":"0x10","var1":"esi"}}' | python asmd.py
```
Hoặc chạy daemon rồi dán JSON từng dòng, Enter để nhận kết quả; Ctrl+Z rồi Enter để thoát.

### HTTP daemon (ASM) – dùng cho VS Code extension
Chạy server HTTP (load model 1 lần):
```
python asmd_http.py
```
Endpoint: `POST http://127.0.0.1:9137/infer`
Body JSON:
```json
{
	"source": "add 0x10 to the current byte in esi",
	"similarity": "add var0 to current byte in var1",
	"var_map": {"var0": "0x10", "var1": "esi"}
}
```
Response: `{ "best": "...", "others": [...], ... }`

Ví dụ PowerShell:
```
$body = '{"source":"add 0x10 to the current byte in esi","similarity":"add var0 to current byte in var1","var_map":{"var0":"0x10","var1":"esi"}}'
curl -Method POST -Uri http://127.0.0.1:9137/infer -Body $body -ContentType 'application/json'
```

### HTTP daemon (Python)
Chạy server HTTP cho model Python:
```
python pyd_http.py
```
Endpoint: `POST http://127.0.0.1:9138/infer`
Body JSON (không dùng var_map nhưng giữ định dạng giống):
```json
{
	"source": "sort list ascending",
	"similarity": "sort var0 ascending",
	"var_map": {}
}
```
Response: `{ "best": "...", "others": [...], ... }`

### Chế độ server/client trong asm_cli
- Server tương đương daemon: `python asm_cli.py --server` (nhận JSON qua stdin, trả JSON).
- Client in ra JSON để pipe: 
```
python asm_cli.py --client --source "..." --similarity "..." --var var0=0x10 --var var1=esi | python asmd.py
```

### Định dạng JSON request
```json
{
	"source": "raw_nl",
	"similarity": "temp_nl",
	"var_map": {"var0": "0x10", "var1": "esi"}
}
```

### Cấu hình
- `USE_KEYSTONE=True`, `NORMALIZE_OUTPUT=True` (đã đặt sẵn). Muốn giảm log transformers: đặt env `TRANSFORMERS_VERBOSITY=error` trước khi chạy.
- Model cache: MODEL_CACHE trong inference_asm.py giúp daemon không reload checkpoint cho mỗi request.

### Lưu ý
- Luôn gửi JSON hợp lệ một dòng; nếu gõ chữ thường ("a") sẽ lỗi parse JSON.
- Best hiện tại: `add byte[esi], 0x10` cho ví dụ trên. Warnings pooler có thể bỏ qua.

### Thay đổi gần nhất
- Thêm asm_cli.py (CLI, server/client), asmd.py (daemon stdin/stdout), cache model, rank/resolve với var_map, keystone optional.
- Thêm asmd_http.py (HTTP daemon) và VS Code extension asm-suggest: chọn text → Ctrl+Alt+A → gửi POST /infer → chèn best, hoặc chọn từ QuickPick.

### VS Code extension (asm-suggest)
1) Chạy HTTP daemon trước:
	- ASM: `python asmd_http.py` (http://127.0.0.1:9137/infer)
	- Python: `python pyd_http.py` (http://127.0.0.1:9138/infer)
2) Cài vsix: `code --install-extension asm-suggest-0.0.4.vsix` (hoặc phiên bản mới nhất).
3) Trong VS Code: chọn đoạn comment/nội dung nguồn → nhấn `Ctrl+Alt+Y` (command: ASM Suggest: Insert from Daemon).
	- Extension gửi JSON `{source: <selection>, similarity: <selection>, var_map: {}}` tới daemon.
	- QuickPick hiện Others (nếu có); chọn để chèn, mặc định chèn Best.
	- Nếu chọn nhiều dòng: mỗi dòng non-empty được gửi riêng, chèn lần lượt các best suggestion (1 dòng source → 1 dòng ASM/Python code).
4) Đổi endpoint (ASM/Python) trong Settings: `asmSuggest.inferUrl` (default 9137). Đặt thành `http://127.0.0.1:9138/infer` để gọi daemon Python.
5) Muốn giảm log transformers: `$env:TRANSFORMERS_VERBOSITY="error"` trước khi chạy daemon.
