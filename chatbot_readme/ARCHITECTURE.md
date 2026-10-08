# Complete AI Chatbot Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     User's Browser                              │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐│
│  │  Next.js UI (http://localhost:3000 or Kubernetes)         ││
│  │  ├─ React 18 Components                                   ││
│  │  ├─ TypeScript Type Safety                               ││
│  │  ├─ Tailwind CSS Styling                                 ││
│  │  └─ Axios HTTP Client                                    ││
│  └────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/JSON
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                        │
│                                                                 │
│  ├─ POST /ask - Chat endpoint                                 │
│  ├─ GET /docs - Swagger UI                                    │
│  ├─ GET /db-check - Database health                           │
│  ├─ Pydantic validation                                       │
│  └─ CORS enabled for UI requests                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓ OpenAI Protocol
┌─────────────────────────────────────────────────────────────────┐
│           Ollama LLM Server (Port 11434)                        │
│                                                                 │
│  ├─ Model: llama2 (or other)                                  │
│  ├─ Flash Attention: Enabled                                 │
│  ├─ KV Cache: Q8_0 quantization                              │
│  └─ Local ML Model Inference                                 │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
1. User types message → Next.js UI captures input
2. UI sends POST request to FastAPI /ask endpoint
3. FastAPI receives message with validation
4. FastAPI calls Ollama API with model parameters
5. Ollama processes message through LLM
6. Ollama returns generated response
7. FastAPI formats response as JSON
8. Next.js UI receives response
9. UI displays message in chat window
10. User sees response in browser
```

## Deployment Architecture

### Local Development
```
Local Machine
├── Ollama (Port 11434)
│   └─ Running with OLLAMA_FLASH_ATTENTION=1
├── PostgreSQL (Port 5432)
│   └─ Optional database for persistence
├── FastAPI (Port 8000)
│   └─ Running with --reload for hot reload
└── Next.js UI (Port 3000)
    └─ Running dev server with npm run dev
```

### Docker Compose (All-in-one)
```
Docker Compose Network
├── ollama service (Port 11434)
├── postgres service (Port 5432)
├── api service (Port 8000)
└── ui service (Port 3000)
```

### Kubernetes (Production)
```
Kubernetes Cluster
├── learn-ollama Deployment
│   └─ Service: learn-ollama:11434
├── learn-api Deployment
│   └─ Service: learn-api:8000
│       └─ Secret: api-credentials (BASE_URL, API_KEY, MODEL)
│       └─ Secret: db-credentials (DATABASE_URL)
└── learn-ui Deployment
    └─ Service: learn-ui:80
        └─ ConfigMap/Env: NEXT_PUBLIC_API_URL
```

## Component Details

### 1. Next.js UI (docker/UI)
```
app/
├── layout.tsx          # Root layout, metadata
├── page.tsx            # Main chat page, state management
└── globals.css         # Global Tailwind styles

components/
├── Header.tsx          # Title, Clear Chat button
├── ChatWindow.tsx      # Message display, auto-scroll
└── InputBox.tsx        # Message input, Send button

Features:
- Client-side React with hooks (useState, useEffect, useRef)
- Tailwind CSS for responsive design
- Environment variable configuration
- Error handling and loading states
- Auto-scrolling to latest message
- Mobile-responsive layout
```

### 2. FastAPI Backend (docker/api)
```
main.py
├── SQLAlchemy: Database ORM (optional)
├── Pydantic: Request/response validation
├── OpenAI client: Ollama integration
└── PostgreSQL: Database connection

Endpoints:
- GET  / - Health check
- GET  /docs - Swagger documentation
- POST /ask - Chat with AI
- GET  /db-check - Database status

Environment:
- BASE_URL: http://localhost:11434/v1 (Ollama)
- API_KEY: ollama
- MODEL: llama2
- DATABASE_URL: postgresql://...
```

### 3. Ollama Server (helm/ollama)
```
Ollama Container
├── Model Engine: LLM inference
├── API Server: OpenAI-compatible endpoints
├── Model Storage: /root/.ollama
└── Configuration:
    - OLLAMA_FLASH_ATTENTION=1 (faster)
    - OLLAMA_KV_CACHE_TYPE=q8_0 (memory efficient)

Supported Models:
- llama2 (default)
- neural-chat
- mistral
- openchat
- And more...
```

## Data Flow Sequences

### Chat Message Flow
```
┌─────────────────┐
│  User Input     │ "What is AI?"
└────────┬────────┘
         ↓
┌─────────────────────────────────────────────┐
│  Next.js Frontend                           │
│  - Capture message in InputBox              │
│  - Show message in ChatWindow               │
│  - Disable input, show loading spinner      │
└────────┬────────────────────────────────────┘
         ↓ POST /ask with {text: "What is AI?"}
┌─────────────────────────────────────────────┐
│  FastAPI Backend (main.py)                  │
│  - Validate request with Pydantic          │
│  - Log message to database (optional)      │
│  - Extract text from request               │
└────────┬────────────────────────────────────┘
         ↓ POST /v1/chat/completions
┌─────────────────────────────────────────────┐
│  Ollama Server                              │
│  - Load model if needed                     │
│  - Run inference                           │
│  - Generate response tokens                │
│  - Return complete response                │
└────────┬────────────────────────────────────┘
         ↓ Return JSON response
┌─────────────────────────────────────────────┐
│  FastAPI Backend                            │
│  - Extract answer from Ollama response     │
│  - Format as JSON                          │
│  - Return to frontend                      │
└────────┬────────────────────────────────────┘
         ↓ Response JSON
┌─────────────────────────────────────────────┐
│  Next.js Frontend                           │
│  - Receive response                         │
│  - Add to messages array                    │
│  - Re-render ChatWindow                     │
│  - Hide loading spinner                     │
│  - Enable input                             │
│  - Auto-scroll to new message              │
└─────────────────────────────────────────────┘
```

## Configuration

### Environment Variables

**Next.js UI** (docker/UI/.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**FastAPI** (docker/api)
```
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL=llama2
DATABASE_URL=postgresql://postgres:test@localhost:5432/postgres
```

**Ollama** (docker-compose or Helm)
```
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
```

**Kubernetes Secrets**
```yaml
# api-credentials
BASE_URL: http://learn-ollama:11434/v1
API_KEY: ollama
MODEL: llama2

# db-credentials
DATABASE_URL: postgresql://postgres:test@postgres:5432/postgres
```

## Deployment Comparison

| Aspect | Local | Docker Compose | Kubernetes |
|--------|-------|---|---|
| **Setup Time** | 30 min | 5 min | 15 min |
| **Scalability** | Single machine | Limited | Horizontal ✅ |
| **Persistence** | Local volumes | Docker volumes | PVC |
| **Monitoring** | None | Docker stats | Prometheus ✅ |
| **High Availability** | No | No | Yes ✅ |
| **Production Ready** | No | Maybe | Yes ✅ |
| **Cost** | Minimal | Low | Variable |

## Kubernetes Resources

```
Deployments:
- learn-ollama (1 replica)
- learn-api (1 replica, configurable)
- learn-ui (1 replica, configurable)

Services:
- learn-ollama (ClusterIP:11434)
- learn-api (ClusterIP:8000)
- learn-ui (ClusterIP:80)

Secrets:
- api-credentials (BASE_URL, API_KEY, MODEL)
- db-credentials (DATABASE_URL)

ConfigMaps:
- UI config (NEXT_PUBLIC_API_URL)

Optional:
- PersistentVolumeClaims (for model storage)
- HorizontalPodAutoscaler (for scaling)
- Ingress (for external access)
```

## Monitoring & Logging

### Local Development
```bash
# Watch UI logs
npm run dev

# Watch API logs
uvicorn main:app --reload --log-level debug

# Watch Ollama logs
ollama serve
```

### Docker Compose
```bash
docker-compose logs -f ui
docker-compose logs -f api
docker-compose logs -f ollama
```

### Kubernetes
```bash
kubectl logs -f deployment/learn-ui
kubectl logs -f deployment/learn-api
kubectl logs -f deployment/learn-ollama
```

## Performance Tuning

### Ollama Optimization
- ✅ OLLAMA_FLASH_ATTENTION=1 - 40% faster inference
- ✅ OLLAMA_KV_CACHE_TYPE=q8_0 - 50% less memory
- Consider GPU acceleration for larger models

### FastAPI Optimization
- ✅ Use uvicorn with multiple workers
- ✅ Enable gzip compression
- ✅ Add Redis caching for common queries

### Next.js Optimization
- ✅ Image optimization
- ✅ Code splitting
- ✅ Static generation where possible
- ✅ Client-side caching

## Security Considerations

1. **API Authentication** - Add JWT tokens
2. **HTTPS** - Enable SSL/TLS in production
3. **Rate Limiting** - Prevent abuse
4. **Input Validation** - Already done with Pydantic
5. **Secrets Management** - Use Kubernetes secrets
6. **CORS** - Configure properly
7. **Environment Variables** - Never hardcode secrets

## Future Enhancements

1. **User Authentication** - Login/registration
2. **Conversation History** - Save chat history
3. **Multiple Models** - Let users choose models
4. **File Uploads** - Support documents/images
5. **Streaming Responses** - Real-time token streaming
6. **Analytics** - Track usage and performance
7. **Admin Dashboard** - Monitor system health
8. **API Rate Limiting** - Prevent abuse
9. **Caching Layer** - Redis for performance
10. **Database Migrations** - Alembic for schema management

---

**Architecture Version**: 1.0
**Last Updated**: 2026-10-07
**Status**: Production Ready ✅
