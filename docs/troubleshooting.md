# Troubleshooting

Common issues and solutions when running INCEPT.sh.

## Server Won't Start

**Symptom:** `incept serve` exits immediately or refuses connections.

**Check llama-server is on PATH:**
```bash
which llama-server
llama-server --version
```

**Check the model file exists:**
```bash
ls -lh /opt/incept-sh/models/incept-sh.gguf
```

**Check port availability:**
```bash
ss -tulpn | grep 8080
```

## Model Not Found

**Symptom:** `ModelNotFoundError` or similar on startup.

**Solution:** Ensure the GGUF file is in the `models/` directory:
```bash
huggingface-cli download 0Time/INCEPT-SH incept-sh.gguf --local-dir ./models
```

## Slow Inference

**Symptom:** Queries take >5 seconds to respond.

**Check available memory:**
```bash
free -h
```

INCEPT.sh requires ~1GB free RAM for the Q8_0 model. If memory is constrained, consider closing other processes or switching to a Q4 quantization.

## Authentication Errors

**Symptom:** `403 Forbidden` from the API.

**Solution:** Verify the API key is set correctly:
```bash
# Start server without auth for testing
incept serve --no-auth

# Or verify your key
curl -H "Authorization: Bearer YOUR_KEY" http://127.0.0.1:8080/v1/health/ready
```

## High Memory Usage

**Symptom:** OOM errors or system slowdown.

INCEPT.sh holds the model in memory for the lifetime of the process (~800MB for Q8_0). This is expected. If you need lower memory usage, use `--no-model` and load on demand, or switch to a smaller quantization.

## Permission Denied

**Symptom:** Cannot write to install directory.

**Solution:**
```bash
sudo chown -R $USER /opt/incept-sh
```

## Getting Help

Open an issue at: https://github.com/0-Time/INCEPT.sh/issues
