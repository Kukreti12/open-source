# Ollama Helm Chart

Deploy Ollama LLM server on Kubernetes.

## Quick Start

### Deploy with default settings
```bash
helm install ollama ./ollama
```

### Deploy with custom settings
```bash
helm install ollama ./ollama \
  --set env.OLLAMA_FLASH_ATTENTION=1 \
  --set env.OLLAMA_KV_CACHE_TYPE=q8_0 \
  --set resources.limits.memory=16Gi
```

## Configuration

Edit `values.yaml` or pass values during install:

### Environment Variables
- `OLLAMA_FLASH_ATTENTION`: Enable flash attention (default: "1")
- `OLLAMA_KV_CACHE_TYPE`: KV cache type (default: "q8_0")

### Resources
```yaml
resources:
  limits:
    cpu: "4"
    memory: "8Gi"
  requests:
    cpu: "2"
    memory: "4Gi"
```

### Persistent Storage
Enable to save downloaded models:
```yaml
persistence:
  enabled: true
  size: 50Gi
  storageClassName: standard  # Change as needed
```

## Enable GPU Support

Add this to `values.yaml`:
```yaml
nodeSelector:
  accelerator: nvidia-gpu
```

Or during install:
```bash
helm install ollama ./ollama --set nodeSelector.accelerator=nvidia-gpu
```

## Access Ollama

### From within cluster
```bash
# API endpoint
http://learn-ollama:11434

# Pull a model
curl http://learn-ollama:11434/api/pull -d '{"name":"llama2"}'

# Generate response
curl http://learn-ollama:11434/api/generate -d '{"model":"llama2","prompt":"hello"}'
```

### Port forward for local access
```bash
kubectl port-forward svc/learn-ollama 11434:11434
```

Then locally:
```bash
# Export API URL
export BASE_URL="http://localhost:11434/v1"
export API_KEY="ollama"
export MODEL="llama2"

# Test
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"llama2","prompt":"hello"}'
```

## Verify Deployment

```bash
# Check pod status
kubectl get pods -l app=learn-ollama

# Check service
kubectl get svc learn-ollama

# Check logs
kubectl logs -l app=learn-ollama -f

# Test health
kubectl exec -it <pod-name> -- curl http://localhost:11434/api/tags
```

## Pull Models into Ollama

```bash
# Port forward first
kubectl port-forward svc/learn-ollama 11434:11434

# Pull model (from another terminal)
curl http://localhost:11434/api/pull -d '{"name":"llama2"}'

# Or use ollama CLI
ollama -b localhost:11434 pull llama2
```

## Integration with FastAPI + Gradio

Update your API deployment values:
```yaml
env:
  BASE_URL: "http://learn-ollama:11434/v1"
  API_KEY: "ollama"
  MODEL: "llama2"
```

## Cleanup

```bash
helm uninstall ollama
```

## Notes

- Ollama requires significant memory (at least 4GB recommended)
- For GPU support, ensure NVIDIA drivers and `nvidia-device-plugin` are installed
- Models are stored in `/root/.ollama` (use PVC for persistence)
- First request will be slow as the model loads into memory
