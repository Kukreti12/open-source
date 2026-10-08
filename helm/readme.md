# Helm Charts for AI Chatbot

This directory contains Helm charts to deploy the AI Chatbot application on Kubernetes.

## 📊 Architecture

```
┌─────────────────────────────────────────────────┐
│         Kubernetes Cluster (Helm Deployed)      │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────┐  ┌──────────┐  ┌──────────┐│
│  │  UI Service    │  │  API Svc │  │ Ollama   ││
│  │ (NodePort)     │  │ (ClusterIP)│ │(Cluster)││
│  │ :30000         │  │ :8000     │  │ :11434  ││
│  └────────────────┘  └──────────┘  └──────────┘│
│         │ (via DNS)   │ (via DNS)   │           │
│         └─────────────┼─────────────┘           │
│                       │                         │
│              Internal Communication             │
│                  (HTTP only)                    │
└─────────────────────────────────────────────────┘
```

## 📁 Chart Structure

```
helm/
├── api/                          # FastAPI Backend
│   ├── Chart.yaml
│   ├── values.yaml              # Configuration
│   └── templates/
│       ├── deployment.yaml      # API deployment with health checks
│       └── service.yaml         # ClusterIP service
│
├── ollama/                       # Ollama LLM Server
│   ├── Chart.yaml
│   ├── values.yaml              # Configuration
│   └── templates/
│       ├── deployment.yaml      # Ollama deployment
│       ├── service.yaml         # ClusterIP service
│       └── pvc.yaml            # Optional persistent storage
│
├── UI/                           # Next.js Frontend
│   ├── Chart.yaml
│   ├── values.yaml              # Configuration
│   └── templates/
│       ├── deployment.yaml      # UI deployment with health checks
│       └── service.yaml         # NodePort service (exposed)
│
└── readme.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Kubernetes cluster (local Docker Desktop, minikube, etc.)
- kubectl configured
- Helm 3.x installed
- Docker images built and available locally

### 1. Build Docker Images

```bash
cd docker/api
docker build -t open-source-api:latest .

cd ../UI
docker build -t open-source-ui:latest .
```

### 2. Deploy with Helm

First, create the namespace:
```bash
kubectl create namespace chatapp
```

Then deploy all three services:

```bash
# Deploy Ollama
helm install ollama ./helm/ollama -n chatapp

# Deploy FastAPI
helm install api ./helm/api -n chatapp

# Deploy UI
helm install ui ./helm/UI -n chatapp
```

Or deploy all at once:
```bash
helm install chatapp ./helm -n chatapp
```

### 3. Verify Deployment

```bash
kubectl get pods -n chatapp
kubectl get svc -n chatapp
```

All pods should show `1/1` Ready status.

### 4. Access the Application

Get the node IP:
```bash
kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}'
```

Open in browser: `http://<NODE_IP>:30000`

## 🔧 Configuration

### API Chart (FastAPI)

Key settings in `helm/api/values.yaml`:

```yaml
image:
  repository: open-source-api      # Docker image name
  tag: latest
  pullPolicy: Never                # Use local images

env:
  BASE_URL: "http://ollama:11434/v1"   # Ollama service DNS
  API_KEY: "ollama"
  MODEL: "qwen:4b"

resources:
  limits:
    cpu: "1000m"
    memory: "1Gi"
```

### Ollama Chart

Key settings in `helm/ollama/values.yaml`:

```yaml
image:
  repository: ollama/ollama
  tag: latest

service:
  port: 11434
  targetPort: 11434
  name: ollama                     # Service DNS name

resources:
  limits:
    cpu: "2000m"
    memory: "4Gi"

livenessProbe:
  path: /api/tags                  # Health check endpoint
  initialDelaySeconds: 30
```

### UI Chart (Next.js)

Key settings in `helm/UI/values.yaml`:

```yaml
image:
  repository: open-source-ui
  tag: latest
  pullPolicy: Never

service:
  type: NodePort
  nodePort: 30000                  # Accessible from host

env:
  NEXT_PUBLIC_API_URL: "http://fastapi:8000"  # API service DNS
```

## 📋 Common Commands

### Helm Operations

```bash
# List releases
helm list -n chatapp

# Show values
helm values api -n chatapp

# Upgrade a release
helm upgrade api ./helm/api -n chatapp

# Rollback
helm rollback api 1 -n chatapp

# Delete
helm uninstall api -n chatapp
helm uninstall ollama -n chatapp
helm uninstall ui -n chatapp
```

### Kubernetes Operations

```bash
# Watch pods
kubectl get pods -n chatapp -w

# Stream logs
kubectl logs -n chatapp -l app=fastapi -f
kubectl logs -n chatapp -l app=ollama -f
kubectl logs -n chatapp -l app=ui -f

# Describe pod
kubectl describe pod -n chatapp <pod-name>

# Port-forward for debugging
kubectl port-forward -n chatapp svc/api 8000:8000
```

## 🆘 Troubleshooting

### Pod won't start
```bash
kubectl describe pod -n chatapp <pod-name>
kubectl logs -n chatapp <pod-name>
```

### Image pull errors
Ensure images are built locally:
```bash
docker images | grep open-source
```

### Service not accessible
Check service status:
```bash
kubectl get svc -n chatapp
kubectl describe svc -n chatapp ui
```

### Certificate warnings
These are informational (Ollama trying to sync with ollama.com). Not critical for local operation.

## 🔐 Certificate Handling

**Internal Communication:** HTTP only (no certificates needed)
- UI ↔ FastAPI: `http://fastapi:8000`
- FastAPI ↔ Ollama: `http://ollama:11434`

**External HTTPS:** (Optional) Not configured by default. For production:
1. Add Ingress resource
2. Use cert-manager with Let's Encrypt
3. Enable TLS in chart values

## 📈 Scaling

Scale services:
```bash
helm upgrade api ./helm/api -n chatapp --set replicaCount=3
helm upgrade ollama ./helm/ollama -n chatapp --set replicaCount=2
```

## 🎯 Service Communication

Services discover each other via Kubernetes DNS:

```
UI Pod
  ↓ (env: NEXT_PUBLIC_API_URL=http://fastapi:8000)
  ↓ Kubernetes DNS resolves to 10.x.x.x
  ↓
FastAPI Pod
  ↓ (env: BASE_URL=http://ollama:11434/v1)
  ↓ Kubernetes DNS resolves to 10.x.x.x
  ↓
Ollama Pod
```

## ✅ Health Checks

All services have health checks configured:

- **FastAPI:** `GET /health` → 200 OK
- **Ollama:** `GET /api/tags` → 200 OK
- **UI:** `GET /` → 200 OK

Pods restart automatically if health checks fail.

## 📝 Installation (Mac)

```bash
brew install helm
```

## 📝 Files Updated

All Helm charts have been updated to work with your local Docker images and include:

- ✅ Health checks for all services
- ✅ Resource limits and requests
- ✅ Environment variable templating
- ✅ Kubernetes DNS service discovery
- ✅ NodePort for UI access
- ✅ ClusterIP for internal services
