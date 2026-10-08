# AI Chatbot - Production Ready Next.js UI

Modern, responsive web interface for the FastAPI chatbot backend built with Next.js, React, and Tailwind CSS.

## Quick Start (Local Development)

### 1. Install dependencies
```bash
npm install
# or
yarn install
```

### 2. Create .env.local file
```bash
echo 'NEXT_PUBLIC_API_URL="http://localhost:8000"' > .env.local
```

### 3. Make sure FastAPI is running
In another terminal:
```bash
cd ../api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run development server
```bash
npm run dev
```

The app will open at `http://localhost:3000`

## Production Build

### Build for production
```bash
npm run build
```

### Start production server
```bash
npm start
```

## Docker Deployment

### Build image
```bash
docker build -t learn-ui:latest .
```

### Run container (local development)
```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://host.docker.internal:8000" \
  learn-ui:latest
```

### Run container (with Docker Compose)
```bash
docker-compose up
```

## Kubernetes Deployment

### Build and push image
```bash
docker build -t saurabhs1/learn:ui-latest .
docker push saurabhs1/learn:ui-latest
```

### Update Helm values
Edit `helm/ui/values.yaml`:
```yaml
image:
  repository: saurabhs1/learn
  tag: ui-latest
  
env:
  NEXT_PUBLIC_API_URL: "http://learn-api:8000"
```

### Deploy with Helm
```bash
helm install ui helm/ui/
```

### Verify deployment
```bash
kubectl get pods -l app=learn-ui
kubectl get svc learn-ui
```

### Access the UI
```bash
kubectl port-forward svc/learn-ui 3000:80
```

Then visit `http://localhost:3000`

## Features

✅ **Production-Ready**: Built with Next.js 14 and modern React patterns
✅ **Responsive Design**: Mobile-first approach with Tailwind CSS
✅ **Type-Safe**: Full TypeScript support
✅ **Auto-scrolling**: Messages auto-scroll to latest
✅ **Real-time Responses**: Streaming AI responses
✅ **Error Handling**: Graceful error messages and recovery
✅ **Loading States**: Visual feedback during processing
✅ **Environment Configuration**: Support for different API endpoints
✅ **Performance**: Optimized builds and lazy loading
✅ **SEO**: Meta tags and semantic HTML

## Project Structure

```
docker/UI/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main chat page
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # Header with clear button
│   ├── ChatWindow.tsx      # Chat messages display
│   └── InputBox.tsx        # Message input
├── public/                 # Static assets
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8000  # FastAPI backend URL
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run export` - Export static HTML (if needed)

## Technologies Used

- **Next.js 14** - React framework with Server Components
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **ESLint** - Code quality

## Performance Optimizations

- Multi-stage Docker build (reduce image size)
- Tree-shaking and code splitting
- Image optimization with Next.js
- CSS minification and purging
- Production builds with SWC compiler

## Deployment

### Development
```bash
npm run dev
```

### Staging/Production with Docker
```bash
docker build -t learn-ui:latest .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL="your-api-url" learn-ui:latest
```

### Kubernetes
See Helm chart in `helm/ui/` for complete Kubernetes deployment
