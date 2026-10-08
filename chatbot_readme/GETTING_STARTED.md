# AI Chatbot - Getting Started Guide

Complete guide to run the production-ready AI Chatbot locally or on Kubernetes.

## Architecture

```
User → Next.js UI (3000) → FastAPI (8000) → Ollama (11434)
```

## Option 1: Local Development (Fastest)

### Prerequisites
- Node.js 18+
- Python 3.11+
- Ollama running: `OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve`

### Step 1: Start FastAPI Backend
```bash
cd docker/api
pip install -r requirements.txt
export DATABASE_URL="postgresql://postgres:test@localhost:5432/postgres"
export BASE_URL="http://localhost:11434/v1"
export API_KEY="ollama"
export MODEL="llama2"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Start Next.js UI
```bash
cd docker/UI
npm install
npm run dev
```

Visit: **http://localhost:3000**

---

## Option 2: Docker Compose (Recommended for Local)

### Start everything with one command
```bash
# From project root
docker-compose up -d
```

This starts:
- Ollama (11434)
- PostgreSQL (5432)
- FastAPI (8000)
- Next.js UI (3000)

### View logs
```bash
docker-compose logs -f ui
docker-compose logs -f api
docker-compose logs -f ollama
```

### Stop services
```bash
docker-compose down
```

Visit: **http://localhost:3000**

---

## Option 3: Kubernetes (Production)

### Prerequisites
- Kubernetes cluster (local minikube or cloud)
- Helm installed

### Deploy all services
```bash
# Deploy Ollama
helm install ollama helm/ollama/

# Deploy FastAPI
helm install api helm/api/

# Deploy Next.js UI
helm install ui helm/ui/

# Verify
kubectl get pods
kubectl get svc
```

### Access the UI
```bash
kubectl port-forward svc/learn-ui 3000:80
```

Visit: **http://localhost:3000**

### Check status
```bash
kubectl get all
kubectl logs -f deployment/learn-ui
```

---

## Development Workflow

### 1. Make changes to Next.js UI
```bash
cd docker/UI
# Edit components, pages, etc.
# Changes auto-reload at http://localhost:3000
```

### 2. Make changes to FastAPI Backend
```bash
cd docker/api
# Edit main.py, etc.
# Changes auto-reload (if using --reload flag)
```

### 3. Build and test Docker images
```bash
# Build UI image
cd docker/UI
docker build -t learn-ui:latest .

# Build API image
cd docker/api
docker build -t learn-api:latest .

# Test with docker-compose
docker-compose up
```

### 4. Push to registry
```bash
docker tag learn-ui:latest saurabhs1/learn:ui-latest
docker push saurabhs1/learn:ui-latest

docker tag learn-api:latest saurabhs1/learn:api-latest
docker push saurabhs1/learn:api-latest
```

---

## Pulling Ollama Models

### Locally
```bash
ollama pull llama2
ollama pull neural-chat
ollama pull mistral
```

### In Kubernetes
```bash
# Port forward Ollama
kubectl port-forward svc/learn-ollama 11434:11434

# Pull model (from another terminal)
curl http://localhost:11434/api/pull -d '{"name":"llama2"}'
```

---

## Environment Variables

### UI (Next.js)
```
NEXT_PUBLIC_API_URL=http://localhost:8000  # API endpoint
```

### API (FastAPI)
```
BASE_URL=http://localhost:11434/v1         # Ollama endpoint
API_KEY=ollama                              # Ollama API key
MODEL=llama2                                # Model to use
DATABASE_URL=...                            # PostgreSQL URL
```

### Ollama
```
OLLAMA_FLASH_ATTENTION=1                    # Enable flash attention
OLLAMA_KV_CACHE_TYPE=q8_0                  # KV cache type
```

---

## Troubleshooting

### UI not connecting to API
```bash
# Check API is running
curl http://localhost:8000/docs

# Check environment variable
cat docker/UI/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Ollama not responding
```bash
# Check Ollama is running
ollama list

# Check port
lsof -i :11434

# Restart Ollama
OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve
```

### Database connection error
```bash
# Check PostgreSQL
psql postgresql://postgres:test@localhost:5432/postgres

# Or use Docker
docker run --rm -it postgres:15 psql postgresql://postgres:test@host.docker.internal:5432/postgres
```

### Port already in use
```bash
# Find process using port
lsof -i :3000  # UI
lsof -i :8000  # API
lsof -i :11434 # Ollama

# Kill process
kill -9 <PID>
```

---

## Production Checklist

- [ ] Build optimized Docker images
- [ ] Push images to registry
- [ ] Configure persistent volumes for Ollama models
- [ ] Set up database backups
- [ ] Configure resource limits in Helm
- [ ] Enable SSL/TLS for HTTPS
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure logging (ELK, Loki)
- [ ] Set up CI/CD pipeline
- [ ] Test auto-scaling

---

## Next Steps

1. **Customize UI**: Edit components in `docker/UI/components/`
2. **Add features**: Extend FastAPI in `docker/api/main.py`
3. **Scale**: Increase replicas in Helm values
4. **Monitor**: Add Prometheus metrics
5. **Deploy**: Push to your Kubernetes cluster

---

## Quick Reference

| Task | Command |
|------|---------|
| Local dev | `docker-compose up` |
| Dev UI only | `cd docker/UI && npm run dev` |
| Build images | `docker-compose build` |
| Deploy K8s | `helm install ui helm/ui/ && helm install api helm/api/` |
| View logs | `kubectl logs -f deployment/learn-ui` |
| Port forward | `kubectl port-forward svc/learn-ui 3000:80` |
| Cleanup | `docker-compose down` / `helm uninstall ui api` |

---

## Support

For issues or questions, check:
- README.md in each component folder
- Docker and Kubernetes documentation
- GitHub Issues
