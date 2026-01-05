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
