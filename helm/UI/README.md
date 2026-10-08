# Next.js Chatbot UI Helm Chart

Deploy the production-ready Next.js chatbot UI on Kubernetes.

## Features

- ✅ Production-ready Next.js 14 application
- ✅ Responsive Tailwind CSS design
- ✅ TypeScript support
- ✅ Multi-stage Docker build (optimized)
- ✅ Auto-scaling ready
- ✅ Health checks configured

## Quick Install

```bash
helm install ui ./ui
```

## Custom Configuration

### Change API URL
```bash
helm install ui ./ui \
  --set env.NEXT_PUBLIC_API_URL="http://learn-api:8000"
```

### Change replica count
```bash
helm install ui ./ui \
  --set replicaCount=3
```

### Change service type to LoadBalancer
```bash
helm install ui ./ui \
  --set service.type=LoadBalancer
```

## Verify Deployment

```bash
# Check pods
kubectl get pods -l app=learn-ui

# Check service
kubectl get svc learn-ui

# Check logs
kubectl logs -l app=learn-ui -f

# Port forward
kubectl port-forward svc/learn-ui 3000:80
```

Visit: `http://localhost:3000`

## Updating the Deployment

### Update image tag
```bash
helm upgrade ui ./ui --set image.tag=v1.0.1
```

### Scale replicas
```bash
kubectl scale deployment learn-ui --replicas=3
```

## Cleanup

```bash
helm uninstall ui
```

## Integration

The UI connects to the FastAPI backend via the `NEXT_PUBLIC_API_URL` environment variable.

Default: `http://learn-api:8000`

Make sure the FastAPI deployment is running in the cluster.
