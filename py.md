


## Infer API examples

### curl (Windows)
```powershell
curl.exe -X POST http://127.0.0.1:9138/infer `
  -H "Content-Type: application/json" `
  -d '{"source":"convert x to hex","similarity":"convert var0 to hex","var_map":{}}'
```

### PowerShell
```powershell
$body = '{"source":"convert x to hex","similarity":"convert var0 to hex","var_map":{}}'

Invoke-RestMethod `
  -Method POST `
  -Uri http://127.0.0.1:9138/infer `
  -ContentType "application/json" `
  -Body $body
```

### Python (`req.py`)
```python
import requests

r = requests.post(
    "http://127.0.0.1:9138/infer",
    json={
        "source": "convert x to hex",
        "similarity": "convert var0 to hex",
        "var_map": {}
    }
)

print(r.json())
```
