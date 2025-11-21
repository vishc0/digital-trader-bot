# GitHub & Deployment Checklist

## ✅ Pre-GitHub Steps

Before pushing to GitHub, ensure:

### 1. Local Testing
```bash
# Test everything locally
docker-compose up -d

# Verify all services are healthy
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8083/health
curl http://localhost:8084/health
curl http://localhost:8085/health

# Stop services
docker-compose down
```

### 2. Git Configuration
```bash
# Initialize git (if not done)
git init

# Configure git user
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Commit
git commit -m "Initial MVP commit: All 6 microservices ready for deployment"

# View status
git status
```

### 3. Push to GitHub
```bash
# If repository doesn't exist, create it on GitHub first
# Then add remote
git remote add origin https://github.com/vishc0/digital-trader-bot.git

# Push to main branch
git branch -M main
git push -u origin main
```

---

## 🚀 GCP Deployment (Recommended for MVP)

### Step 1: Setup GCP Project

```bash
# Set project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  build.googleapis.com \
  container.googleapis.com \
  memorystore.googleapis.com

# Create Redis instance
gcloud redis instances create trading-redis \
  --size=2 \
  --region=us-central1
```

### Step 2: Build & Push Docker Images

```bash
# Build state manager
gcloud builds submit \
  --config=cloudbuild.yaml \
  --tag gcr.io/YOUR-PROJECT-ID/state-manager:latest

# Build other services
for service in strategy_engine wisdom_builder external_intelligence journaling_service data_handler; do
  gcloud builds submit src/$service \
    --tag gcr.io/YOUR-PROJECT-ID/$service:latest
done
```

### Step 3: Deploy to Cloud Run

```bash
# Get Redis IP
REDIS_IP=$(gcloud redis instances describe trading-redis \
  --region=us-central1 \
  --format='value(host)')

# Deploy State Manager
gcloud run deploy state-manager \
  --image gcr.io/YOUR-PROJECT-ID/state-manager:latest \
  --memory 512Mi \
  --cpu 1 \
  --port 8080 \
  --set-env-vars REDIS_HOST=$REDIS_IP,MAX_DAILY_LOSS=-500.00 \
  --region us-central1 \
  --allow-unauthenticated

# Deploy other services
gcloud run deploy strategy-engine \
  --image gcr.io/YOUR-PROJECT-ID/strategy_engine:latest \
  --memory 512Mi --region us-central1 --allow-unauthenticated

gcloud run deploy wisdom-builder \
  --image gcr.io/YOUR-PROJECT-ID/wisdom_builder:latest \
  --memory 512Mi --region us-central1 --allow-unauthenticated

gcloud run deploy external-intelligence \
  --image gcr.io/YOUR-PROJECT-ID/external_intelligence:latest \
  --memory 512Mi --region us-central1 --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$YOUR_GEMINI_API_KEY

gcloud run deploy journaling-service \
  --image gcr.io/YOUR-PROJECT-ID/journaling_service:latest \
  --memory 512Mi --region us-central1 --allow-unauthenticated

gcloud run deploy data-handler \
  --image gcr.io/YOUR-PROJECT-ID/data_handler:latest \
  --memory 512Mi --region us-central1 --allow-unauthenticated
```

### Step 4: Setup CI/CD with Cloud Build

The `cloudbuild.yaml` file will trigger automatic deployments on `git push`.

---

## 🔧 AWS Deployment (Alternative)

### Step 1: Setup AWS Account

```bash
# Configure AWS CLI
aws configure

# Create ECR repositories
aws ecr create-repository --repository-name state-manager
aws ecr create-repository --repository-name strategy-engine
# ... repeat for other services
```

### Step 2: Build & Push to ECR

```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t state-manager src/state_manager/
docker tag state-manager:latest YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/state-manager:latest
docker push YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/state-manager:latest
```

### Step 3: Deploy with Lambda/ECS

```bash
# Create Lambda function for each service
# Or use ECS for container orchestration
# See docs/AWS_DEPLOYMENT.md for detailed instructions
```

---

## 🧪 Local Development Setup

### First Time Setup

```bash
# Clone repository
git clone https://github.com/vishc0/digital-trader-bot.git
cd digital-trader-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Docker services
docker-compose up -d

# Verify setup
docker-compose ps
```

### Daily Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Modifying Code

```bash
# Edit code in src/ directories
# Services auto-reload in development mode

# Rebuild specific service
docker-compose build state-manager
docker-compose up -d state-manager
```

---

## 📊 Monitoring & Debugging

### Check Service Health

```bash
# All services
for port in 8080 8081 8082 8083 8084 8085; do
  echo "Port $port:"
  curl http://localhost:$port/health 2>/dev/null | jq .
done

# Or individually
curl http://localhost:8080/health | jq .
```

### View Logs

```bash
# Docker Compose logs
docker-compose logs state-manager
docker-compose logs strategy-engine

# Tail logs
docker-compose logs -f state-manager

# GCP Cloud Run logs
gcloud run logs read state-manager --limit 50

# AWS CloudWatch logs
aws logs tail /aws/lambda/state-manager --follow
```

### Test Endpoints

```bash
# Market state
curl http://localhost:8080/market-state

# Generate signals
curl -X POST http://localhost:8081/signals \
  -H "Content-Type: application/json" \
  -d '{}'

# Daily PnL
curl http://localhost:8080/daily-pnl

# Market snapshot
curl http://localhost:8085/snapshot
```

---

## 🔑 Environment Variables

### Required Variables

```bash
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Safety
MAX_DAILY_LOSS=-500.00

# Application
APP_ID=algo_brain_v1

# LLM (for External Intelligence)
GEMINI_API_KEY=your_key_here

# Deployment
PORT=8080  # Each service has different port
```

### Setting in Different Environments

**Local (docker-compose.yml):**
```yaml
environment:
  - REDIS_HOST=redis
  - MAX_DAILY_LOSS=-500.00
```

**GCP (gcloud command):**
```bash
--set-env-vars KEY1=value1,KEY2=value2
```

**AWS (Lambda environment variables):**
```bash
aws lambda update-function-configuration \
  --function-name state-manager \
  --environment Variables={REDIS_HOST=localhost,MAX_DAILY_LOSS=-500.00}
```

---

## 🚨 Troubleshooting Deployment

### Docker Images Won't Build
```bash
# Clean up old images
docker system prune -a

# Rebuild with verbose output
docker-compose build --verbose

# Check Dockerfile syntax
docker run --rm -i hadolint/hadolint < Dockerfile
```

### Services Not Starting
```bash
# Check logs
docker-compose logs

# Ensure Redis is running
docker-compose ps redis

# Restart everything
docker-compose down
docker-compose up -d
```

### Connection Issues
```bash
# Test Redis connection
redis-cli ping

# Check network
docker network ls
docker network inspect trading-network

# Restart network
docker network rm trading-network
docker-compose up -d
```

### Port Conflicts
```bash
# Find what's using port
lsof -i :8080
netstat -tulpn | grep 8080  # Linux
netstat -ano | findstr :8080  # Windows

# Use different ports in docker-compose.yml
# Or kill conflicting process
kill -9 <PID>
```

---

## ✅ Pre-Production Checklist

- [ ] All 6 services tested locally
- [ ] Docker Compose setup verified
- [ ] GCP/AWS credentials configured
- [ ] Gemini API key set
- [ ] Max daily loss limit configured ($500 is default)
- [ ] Git repository created on GitHub
- [ ] Initial commit pushed
- [ ] Cloud Build/CodePipeline configured
- [ ] Monitoring/alerting setup
- [ ] Backup strategy defined
- [ ] Rollback procedure documented
- [ ] Load testing completed
- [ ] Security audit passed

---

## 📞 Deployment Support

For issues:
1. Check logs: `docker-compose logs`
2. Review ARCHITECTURE.md for service details
3. Check API endpoints with curl/Postman
4. Verify environment variables are set
5. Ensure Redis is accessible
6. Check network connectivity between services

---

**Ready to Deploy!** ✅

Push to GitHub, then deploy to GCP Cloud Run or AWS Lambda.
