## Resources model

# Paper code (Chinese)

- pretrain or full: [train](https://www.kaggle.com/code/datvutyn/notebook2fd53223e8) (nhưng timeout 12h) - đã có dapt, tapt, assembly

- [python](https://www.kaggle.com/code/thnhtvng/final)

- assembly: lấy từ pretrain, checkpoint để làm tiếp - [assembly](https://www.kaggle.com/code/vuongdat67/assemblyc)

- [Model folder](https://drive.google.com/file/d/1KUYjf7CJHov_03QcQ7OZX5hqmQ-BBNtS/view?usp=sharing)

- [Demo YT 1 line](https://youtu.be/4-AwYVKcXZ8)

- [Demo YT multi line](https://youtu.be/lRZLO8oVCbA)

# My improvement (English)

- [dapt](https://www.kaggle.com/datasets/thnhtvng/daptmodel/)
  
- [tapt](https://www.kaggle.com/code/thnhtvng/pretrained-model/)

- full pretrain_mode: [model fg-codebert pretrain](https://www.kaggle.com/datasets/vuongdat67/pretrain-model/) and [code](https://www.kaggle.com/code/vuongdat67/pretrained-model)
  
- [python](https://www.kaggle.com/code/datvutyn/python)
  
- [assembly](https://www.kaggle.com/code/datvutyn/assembly)
  
- [code](https://www.kaggle.com/datasets/datvutyn/codetrain/)
  
- [datasets](https://www.kaggle.com/datasets/datvutyn/exploitgen-data/)

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


# Cli 

## Server

```bash
python asm_cli.py --server
```

## Client pipe qua daemon:

```bash
python asm_cli.py --client --source "add 0x10..." --similarity "add var0..." --var var0=0x10 --var var1=esi | python asmd.py
```

## Chạy trực tiếp (không daemon):

```bash
python asm_cli.py --source "add 0x10 to the current byte in esi" --similarity "add var0 to current byte in var1" --var var0=0x10 --var var1=esi --json
```

```bash
python asmd.py 

{"source":"add 0x10 to the current byte in esi","similarity":"add var0 to current byte in var1","var_map":{"var0":"0x10","var1":"esi"}}
```

```bash
$env:TRANSFORMERS_VERBOSITY="error"
```
