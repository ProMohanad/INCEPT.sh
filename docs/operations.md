# Operations Guide

## Health Checks

INCEPT.sh exposes two health endpoints when running in server mode:

- `GET /v1/health/live` — liveness check (always returns 200 if the process is running)
- `GET /v1/health/ready` — readiness check (returns 200 only when the model is loaded and ready)

```bash
curl http://127.0.0.1:8080/v1/health/ready
```

## Monitoring

### systemd

```bash
# Check service status
systemctl status incept-sh

# View logs
journalctl -u incept-sh -f
```

### Log Format

Logs are written to stdout/stderr in structured JSON format:

```json
{"timestamp": "2026-03-09T12:00:00Z", "level": "INFO", "message": "Model loaded", "duration_ms": 1240}
```

## Alerting

| Condition | Severity |
|---|---|
| `/v1/health/ready` returns non-200 | Critical |
| Inference latency > 5s | Warning |
| Memory usage > 80% | Warning |

## Rollback

Restore a previous model version by replacing `models/incept-sh.gguf` with a backup and restarting the service:

```bash
cp models/incept-sh.gguf.bak models/incept-sh.gguf
systemctl restart incept-sh
```

## Scaling

INCEPT.sh is stateless and CPU-bound. Horizontal scaling is straightforward — run multiple instances behind a load balancer, each with their own model copy.
