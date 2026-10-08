# 🚀 AI Chatbot - Quick Start (5 minutes)

## Choose Your Path

### 🏃 Path 1: Docker Compose (Easiest)
**One command to run everything:**

```bash
cd /Users/ssharma/Downloads/learning/open-source
docker-compose up
```

Done! Visit: **http://localhost:3000**

### 💻 Path 2: Local Development (Recommended for Development)

**Terminal 1: Start Ollama** (if not already running)
```bash
OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve
```

**Terminal 2: Start FastAPI**
```bash
cd docker/api
pip install -r requirements.txt
export BASE_URL="http://localhost:11434/v1"
export API_KEY="ollama"
export MODEL="llama2"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3: Start Next.js UI**
```bash
cd docker/UI
npm install
npm run dev
```

Visit: **http://localhost:3000**

### ☸️  Path 3: Kubernetes (Production)

```bash
# Deploy all services
helm install ollama helm/ollama/
helm install api helm/api/
helm install ui helm/ui/

# Port forward to access locally
kubectl port-forward svc/learn-ui 3000:80
```

Visit: **http://localhost:3000**

---

## 🎯 What Just Happened?

You now have a complete AI chatbot running with:

- **UI**: Modern Next.js React app (Responsive, Fast, Beautiful)
- **API**: FastAPI backend (Type-safe, Fast, Scalable)
- **LLM**: Ollama server (Local AI model, Private, Optimized)
- **DB**: PostgreSQL (Optional, for persistence)

```
Browser → Next.js UI → FastAPI API → Ollama LLM
(3000)       (8000)       (11434)
```

---

## 📝 First Chat

1. Open **http://localhost:3000** in your browser
2. Type: `Hello, who are you?`
3. Press Enter or click Send
4. Watch the AI respond

---

## 🛠️ Next Steps

| Task | Command |
|------|---------|
| View UI logs | `docker-compose logs -f ui` |
| View API logs | `docker-compose logs -f api` |
| View Ollama logs | `docker-compose logs -f ollama` |
| Stop services | `docker-compose down` |
| Pull different model | `curl http://localhost:11434/api/pull -d '{"name":"mistral"}'` |
| Scale API to 3 instances | `helm upgrade api helm/api/ --set replicaCount=3` |
| Build UI for production | `cd docker/UI && npm run build` |

---

## 🐛 Troubleshooting

### UI blank/not loading?
```bash
# Check API is running
curl http://localhost:8000/docs

# Check logs
docker-compose logs ui
```

### API returning errors?
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check logs
docker-compose logs api
```

### Port already in use?
```bash
# Find what's using port 3000
lsof -i :3000

# Kill it
kill -9 <PID>
```

---

## 📚 Full Documentation

- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - Complete setup guide
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design & data flow
- **[NEXTJS_UI_SUMMARY.md](./NEXTJS_UI_SUMMARY.md)** - UI details
- **[docker/UI/README.md](./docker/UI/README.md)** - UI documentation
- **[docker/api/README.md](./docker/api/README.md)** - API documentation
- **[helm/*/README.md](./helm)** - Kubernetes documentation

---

## 🎨 Customize

### Change Colors
Edit `docker/UI/tailwind.config.js`

### Add Features
Edit React components in `docker/UI/components/`

### Change API Endpoint
Edit `docker/UI/.env.local`

### Deploy to Production
Push to your registry and deploy with Helm

---

## ✅ You're Ready!

Your AI chatbot is now running. Start chatting! 🤖

Need help? Check the documentation files or re-run the appropriate setup command above.

---

**Setup Time**: ~5 minutes
**Resources**: ~2GB RAM, ~10GB disk
**Cost**: Free (self-hosted)
**Status**: ✅ Production Ready
