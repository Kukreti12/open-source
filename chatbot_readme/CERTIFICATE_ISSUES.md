# Kubernetes Certificate Issues - Detailed Explanation

## The Problem We Saw

```
WARN source=model_show_cache.go:144 msg="model show cloud cache hydration failed" 
error="Get \"https://ollama.com:443/api/tags?ts=1791413324\": tls: failed to verify certificate: x509: certificate signed by unknown authority"
```

## Why This Happens

Ollama tries to fetch model recommendations from `ollama.com` via HTTPS. However:

1. **The container image doesn't have CA certificates** - When running in a minimal container, the system CA store might be missing
2. **Self-signed certificates** - If you're using self-signed certs internally, the container won't trust them
3. **Certificate path issues** - The container can't find the CA bundle file

## Certificate Issues in Kubernetes

### 1. Internal Service-to-Service Communication (What You're Using)
✅ **No certificate issues** - All services talk via HTTP internally
```
UI → fastapi:8000 (HTTP)
FastAPI → ollama:11434 (HTTP)
```

### 2. External HTTPS Access (Advanced Scenario)
⚠️ **Certificate issues possible** - If you expose services with TLS

### 3. Calling External APIs (What Ollama Encountered)
❌ **Certificate validation needed** - Ollama tries to call `ollama.com` via HTTPS

## Solutions

### Solution 1: Fix for Ollama (Recommended)
Update the Ollama deployment to include CA certificates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: chatapp
spec:
  template:
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        env:
        - name: SSL_NO_VERIFY  # Disable SSL verification (not recommended for prod)
          value: "false"
        # OR add CA certificates via ConfigMap
      volumes:
      - name: ca-certs
        configMap:
          name: ca-certificates
```

### Solution 2: Disable External API Calls (Quickest)
Set environment variables to prevent external calls:

```yaml
env:
- name: OLLAMA_INSECURE
  value: "true"
```

### Solution 3: Proper HTTPS with Let's Encrypt (Production)

If you need production-grade HTTPS:

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Solution 4: Self-Signed Certificate Setup

```bash
# Create self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout tls.key -out tls.crt -days 365 -nodes \
  -subj "/CN=ollama.local"

# Create Kubernetes secret
kubectl create secret tls ollama-tls --cert=tls.crt --key=tls.key -n chatapp

# Reference in Ingress
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ollama-ingress
  namespace: chatapp
spec:
  tls:
  - hosts:
    - ollama.local
    secretName: ollama-tls
  rules:
  - host: ollama.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ollama
            port:
              number: 11434
EOF
```

## Current Deployment - NO CERTIFICATE ISSUES ✅

Your current setup has **NO certificate problems** because:

1. ✅ All internal services use HTTP (no TLS validation needed)
2. ✅ Services discover each other via Kubernetes DNS
3. ✅ The warning about ollama.com is just for optional cloud sync
4. ✅ Your FastAPI ↔ Ollama communication works fine

## Troubleshooting Commands

### Check if CA certificates are available in container
```bash
kubectl exec -it -n chatapp $(kubectl get pod -n chatapp -l app=ollama -o jsonpath='{.items[0].metadata.name}') -- ls -la /etc/ssl/certs/
```

### Check certificate details
```bash
kubectl get secret ollama-tls -n chatapp -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

### Test certificate validation
```bash
kubectl exec -it -n chatapp deployment/ollama -- openssl s_client -connect ollama.com:443
```

### View all Kubernetes secrets
```bash
kubectl get secrets -n chatapp
```

## Summary

| Aspect | Your Setup | Status |
|--------|-----------|--------|
| Internal HTTP communication | ✅ Yes | ✓ Works |
| Certificate validation needed | ❌ No | ✓ No issues |
| External HTTPS calls | ⚠️ Ollama→ollama.com | ⚠️ Warning only |
| Production HTTPS support | ❌ Not configured | Can add with Ingress+Cert-Manager |
| Service discovery | ✅ DNS | ✓ Works |

The warning message is **not a blocker** - Ollama works fine without cloud cache sync. It's just informational.
