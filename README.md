<div align="center">

```
██╗███╗   ██╗ ██████╗███████╗██████╗ ████████╗ ┃ ███████╗██╗  ██╗
██║████╗  ██║██╔════╝██╔════╝██╔══██╗╚══██╔══╝ ┃ ██╔════╝██║  ██║
██║██╔██╗ ██║██║     █████╗  ██████╔╝   ██║    ┃ ███████╗███████║
██║██║╚██╗██║██║     ██╔══╝  ██╔═══╝    ██║    ┃ ╚════██║██╔══██║
██║██║ ╚████║╚██████╗███████╗██║        ██║    ┃ ███████║██║  ██║
╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝        ╚═╝    ┃ ╚══════╝╚═╝  ╚═╝
```

**Offline Natural Language → Linux Command Engine**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Model](https://img.shields.io/badge/model-Qwen3.5--0.8B-orange.svg)](https://huggingface.co/Qwen/Qwen3.5-0.8B)
[![Score](https://img.shields.io/badge/benchmark-99%2F100-brightgreen.svg)](#benchmark)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

</div>

---

Type what you want in plain English. Get the exact Linux command back. No internet. No cloud. No guessing.

```bash
INCEPT/Sh ❯ find all python files modified in the last 7 days
  ✓ SAFE   $ find . -name "*.py" -mtime -7

INCEPT/Sh ❯ grep for email addresses in contacts.csv
  ✓ SAFE   $ grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' contacts.csv

INCEPT/Sh ❯ show all open ports and which process is using them
  ✓ SAFE   $ sudo netstat -tulpn

INCEPT/Sh ❯ add text at line 1000 of hello.txt
  ✓ SAFE   $ sed -i '1000a\ your text here' hello.txt
```

## What is this?

INCEPT/Sh is a fine-tuned **Qwen3.5-0.8B** model (774MB, Q8_0 GGUF) that translates plain English into Linux shell commands — entirely offline, on your machine, with no API calls.

- **99/100** on a 100-question Linux command benchmark
- **~1–2 seconds** per query on Apple M4 (CPU inference)
- **No hallucinated commands** — safety layer blocks non-command output
- **Prompt injection defense** — responds `UNSAFE_REQUEST` to manipulation attempts
- Supports Ubuntu, Debian, RHEL, Arch, Fedora, CentOS, openSUSE

## Quick Start

### Requirements

- Python 3.11+
- [llama-cli](https://github.com/ggerganov/llama.cpp) (brew install llama.cpp on macOS, or build from source)
- ~1GB free RAM

### Install

```bash
git clone https://github.com/ProMohanad/INCEPT.sh
cd INCEPT.sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[cli]"
```

### Get the Model

Download the fine-tuned model (774MB):

> **Coming soon** — model will be released on Hugging Face.

Place it in the `models/` directory:

```bash
mkdir -p models
cp incept-command-v2-q8_0.gguf models/
```

### Run

```bash
# Interactive REPL
incept

# One-shot query
incept -c "list all running docker containers"

# Minimal output (pipe-friendly)
incept -c "show disk usage" -m

# Generate and execute immediately
incept -c "show memory usage" --exec
```

## CLI Reference

```
incept [OPTIONS] 

Options:
  -c, --command TEXT   One-shot query (non-interactive)
  -m, --minimal        Output command only (no UI chrome)
  --exec               Generate command and prompt to execute
  --help               Show this message and exit
```

Interactive slash commands:

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/context` | Show current system context |
| `/exit` | Exit |

## How It Works

1. Your query goes to the fine-tuned model via **llama.cpp**
2. Output is post-processed: first line only, prose stripped, injections blocked
3. Risk classification: `SAFE` / `CAUTION` / `DANGEROUS` / `BLOCKED`
4. You choose to `[E]xecute`, `[C]opy`, or dismiss

The model was trained on **79,000+ ChatML examples** across 6 Linux distros, then further refined with **8,500 targeted examples** fixing path over-specification, prompt injection, and prose leakage.

## Benchmark

Evaluated on 100 real-world Linux command queries (Ubuntu 22.04, bash, non-root context):

| Model Version | Score |
|--------------|-------|
| SFT v1 (baseline) | 73/100 |
| SFT v2 (79K examples) | 75/100 |
| SFT v2 + benchmark fixes | 93/100 |
| SFT v2 + safety layer | 94/100 |
| **Production (current)** | **99/100** |

The one remaining failure: Q74 returns `systemctl poweroff` instead of `reboot` — both are valid Linux commands for the same intent.

## Safety

- **Prompt injection defense**: any attempt to manipulate the model returns `UNSAFE_REQUEST`
- **Prose detection**: non-command English output is suppressed
- **Risk badges**: every command is risk-classified before display
- **No network calls**: zero outbound traffic at runtime

## Training

The model is a LoRA fine-tune of [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) (hybrid Mamba/attention architecture).

| Parameter | Value |
|-----------|-------|
| Base model | Qwen/Qwen3.5-0.8B |
| Training examples | 79,264 (SFT) + 8,576 (production refinement) |
| LoRA rank | 16 |
| Quantization | Q8_0 (774MB) |
| Inference temp | 0.0 (greedy) |
| Training hardware | Apple M4 Mac mini, 32GB (CPU, ~50 min/epoch) |

## Project Structure

```
incept/
├── cli/        # CLI entry point, banner, REPL
├── core/       # Engine, model loader, context detection
configs/        # Training configs
scripts/        # Benchmark and evaluation scripts
models/         # GGUF model files (not included in repo)
data/           # Training data (not included in repo)
```

## Known Issues

- **llama-cpp-python 0.3.16** does not support Qwen3.5 GGUF natively — the engine falls back to `llama-server` subprocess automatically
- Mamba (SSM) layers have no MPS Metal kernels — training runs on CPU via BLAS

## License

[Apache License 2.0](LICENSE)

---

<div align="center">
Built with 🐧 on Apple Silicon
</div>
