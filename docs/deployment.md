# Deployment Guide

INCEPT.sh is deployed as a standalone CLI tool or optional REST API server. No containerization required.

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/0-Time/INCEPT.sh/main/install.sh | bash
```

The installer handles all dependencies including Python 3.11+, llama-server, and the model download.

## Manual Installation

See the [README](../README.md#installation) for step-by-step instructions.

## Server Mode

INCEPT.sh includes an optional FastAPI server for REST API access:

```bash
incept serve --host 127.0.0.1 --port 8080
```

### Reverse Proxy (nginx)

```nginx
server {
    listen 443 ssl;
    server_name incept.example.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 30s;
    }
}
```

### systemd Service

```ini
[Unit]
Description=INCEPT.sh API Server
After=network.target

[Service]
Type=simple
User=incept
ExecStart=/usr/local/bin/incept serve --host 127.0.0.1 --port 8080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Requirements

- Linux x86_64 or aarch64
- Python 3.11+
- llama-server (installed by install.sh)
- ~1GB RAM at runtime
