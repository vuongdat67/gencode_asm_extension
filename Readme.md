# Usage Guide

## 1. Backend Setup (Python)

### Create virtual environment
```bash
python -m venv .venv
````

Activate venv:

* **Windows**

```bash
.venv\Scripts\activate
```

* **Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run backend API

```bash
python asmd_http.py
```

---

## 2. VS Code Extension Setup (Node.js)

### Install dependencies

```bash
npm install
```

### Compile & watch extension

```bash
npm run compile
npm run watch
```

> Press **F5** to start **Extension Development Host** for debugging.

---

## 3. Run Tests

```bash
pytest
```

---

## 4. Package & Install Extension

> Make sure `vsce` is installed:

```bash
npm install -g @vscode/vsce
```

### Package extension

```bash
npx vsce package
```

### Install extension

```bash
code --install-extension asm-suggest-0.0.2.vsix
```


## Resources model

pretrain or full: https://www.kaggle.com/code/datvutyn/notebook2fd53223e8 (nhưng timeout 12h) - đã có dapt, tapt, assembly
python: https://www.kaggle.com/code/thnhtvng/final
assembly: lấy từ pretrain, checkpoint để làm tiếp - https://www.kaggle.com/code/vuongdat67/assemblyc

[Model folder](https://drive.google.com/file/d/1lrfN5c5rmJzP0ou4JCOVPpbOZ0grS4F8/view?usp=drive_link)

[Demo YT 1 line](https://youtu.be/4-AwYVKcXZ8)

[Demo YT multi line](https://youtu.be/lRZLO8oVCbA)


# Cli 

## Server

python asm_cli.py --server

## Client pipe qua daemon:
python asm_cli.py --client --source "add 0x10..." --similarity "add var0..." --var var0=0x10 --var var1=esi | python asmd.py

## Chạy trực tiếp (không daemon):
python asm_cli.py --source "add 0x10 to the current byte in esi" --similarity "add var0 to current byte in var1" --var var0=0x10 --var var1=esi --json

python asmd.py
{"source":"add 0x10 to the current byte in esi","similarity":"add var0 to current byte in var1","var_map":{"var0":"0x10","var1":"esi"}}


$env:TRANSFORMERS_VERBOSITY="error"