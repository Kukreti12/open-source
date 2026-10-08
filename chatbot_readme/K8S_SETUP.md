# Kubernetes Deployment Guide

## Current Status
✅ Your application is now running on Kubernetes!

**Access Points:**
- **UI:** http://192.168.65.3:30000
- **FastAPI (internal):** http://fastapi:8000 (within cluster)
- **Ollama (internal):** http://ollama:11434 (within cluster)

## Kubernetes Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Kubernetes Cluster               │
│                   (chatapp namespace)                │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────┐│
│  │     UI       │   │   FastAPI    │   │  Ollama  ││
│  │   (Node: 3k) │   │ (Cluster IP) │   │(Cluster) ││
│  │ :30000       │   │ :8000        │   │  :11434  ││
│  └──────┬───────┘   └──────┬───────┘   └────┬─────┘│
│         │                  │                 │      │
│         └──────────────────┼─────────────────┘      │
│              Internal DNS Resolution                 │
│          (service discovery via k8s DNS)             │
└─────────────────────────────────────────────────────┘
```

## Certificate Issues & Solutions

### Problem
When exposing Ollama or other services via HTTPS/TLS in Kubernetes, certificate validation can fail because:

1. **Self-signed certificates** - Clients don't trust the CA
2. **Certificate hostname mismatch** - Service name doesn't match certificate CN
3. **Internal vs External access** - Different URLs for internal/external access
4. **Mutual TLS (mTLS)** complexity in microservices

### Current Setup (No HTTPS)
- All services communicate over HTTP internally
- UI is exposed via NodePort (no TLS)
- Perfect for development/internal testing

### Optional: HTTPS Setup (If Needed)

If you need HTTPS, uncomment the Ingress manifest in `k8s/ingress-tls.yaml` (created below).

## Service Communication Flow

```
Browser Request (HTTP)
    ↓
UI Pod (Next.js port 3000)
    ↓ HTTP request to /api/ask
Next.js Server (handles proxy)
    ↓ HTTP request to fastapi:8000
FastAPI Pod (port 8000)
    ↓ HTTP request to ollama:11434
Ollama Pod (port 11434)
    ↓
Response returned to browser
```

## Kubernetes DNS

All pods can resolve each other via internal DNS:
- `http://ollama:11434` → resolves to 10.96.128.252
- `http://fastapi:8000` → resolves to 10.102.194.3
- Service discovery is automatic!

## Helpful Commands

### Check status
```bash
kubectl get pods -n chatapp
kubectl get svc -n chatapp
kubectl logs -n chatapp -l app=ui
kubectl logs -n chatapp -l app=fastapi
kubectl logs -n chatapp -l app=ollama
```

### Port-forward for debugging
```bash
kubectl port-forward -n chatapp svc/fastapi 8000:8000
kubectl port-forward -n chatapp svc/ollama 11434:11434
```

### Describe resources
```bash
kubectl describe deployment -n chatapp
kubectl describe svc -n chatapp
```

### Clean up
```bash
kubectl delete namespace chatapp
```

## Environment Variables

### FastAPI Pod
- `DATABASE_URL`: postgresql://postgres:test@localhost:5432/postgres
- `BASE_URL`: http://ollama:11434/v1 (Kubernetes service DNS)
- `API_KEY`: ollama
- `MODEL`: qwen:4b

### UI Pod
- `NEXT_PUBLIC_API_URL`: http://fastapi:8000 (internal for server-side requests)
- Client-side requests go to `/api/ask` (proxied by Next.js server)

## Scaling

To scale services:
```bash
kubectl scale deployment ollama -n chatapp --replicas=3
kubectl scale deployment fastapi -n chatapp --replicas=2
```

## Next Steps

1. **Test the UI:** Go to http://192.168.65.3:30000
2. **Send a message** - It should route through FastAPI to Ollama
3. **Monitor logs:** `kubectl logs -n chatapp -l app=fastapi -f`
4. **For HTTPS:** See optional ingress configuration below
