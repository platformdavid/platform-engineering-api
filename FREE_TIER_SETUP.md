# 🆓 Free Tier Platform Engineering Setup

This guide shows you how to set up a **complete Platform Engineering API** using **100% free tools** for your tech test. No money required!

## 🎯 Free Tier Strategy

**Why Free Tier?** This actually demonstrates **cost optimization** - a key skill for platform engineers at companies like FanDuel!

### **Free Alternatives Used:**

| **Component** | **Paid Option** | **Free Alternative** | **Why Better for Test** |
|---------------|-----------------|---------------------|-------------------------|
| **CI/CD** | BuildKite ($15/agent/month) | **GitHub Actions** (2000 min/month free) | Industry standard, unlimited public repos |
| **Container Registry** | AWS ECR ($0.10/GB) | **GitHub Container Registry** (unlimited) | Integrated with GitHub Actions |
| **Kubernetes** | EKS ($0.10/hour) | **Minikube/Docker Desktop** (free) | Local development, no cloud costs |
| **Monitoring** | Grafana Cloud ($49/month) | **Local Prometheus + Grafana** (free) | Full control, no limits |
| **Code Quality** | SonarQube ($10/month) | **SonarCloud** (free for public repos) | Same features, zero cost |
| **Database** | RDS ($13/month) | **Local PostgreSQL** (free) | No network latency, instant setup |

## 🚀 Quick Free Setup

### **1. Prerequisites (All Free)**

```bash
# Install free tools
# - Python 3.11+ (free)
# - Docker Desktop (free)
# - Git (free)
# - VS Code (free)
# - PostgreSQL (free)

# Optional but recommended:
# - Minikube (free local Kubernetes)
# - kubectl (free)
# - Terraform (free)
```

### **2. Environment Setup**

```bash
# Copy environment template
cp env.example .env

# Edit with your free credentials
nano .env
```

**Free Environment Variables:**

```env
# Database (Local PostgreSQL - FREE)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/platform_engineering_db

# AWS (Your existing account - FREE tier for 12 months)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# GitHub (FREE - unlimited public repos)
GITHUB_TOKEN=your-github-token
GITHUB_ORGANIZATION=platformdavid

# Local Kubernetes (FREE)
K8S_NAMESPACE=platform-engineering
K8S_CLUSTER_NAME=platformdavid-local
CONTAINER_REGISTRY_URL=ghcr.io/platformdavid

# Local Monitoring (FREE)
GRAFANA_URL=http://localhost:3000
PROMETHEUS_URL=http://localhost:9090

# SonarCloud (FREE for public repos)
SONARCLOUD_TOKEN=your-sonarcloud-token
SONARCLOUD_ORGANIZATION=platformdavid
```

### **3. Database Setup (Free)**

```bash
# Option 1: Local PostgreSQL (FREE)
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres createdb platform_engineering_db

# Option 2: Docker PostgreSQL (FREE)
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=platform_engineering_db \
  -p 5432:5432 \
  postgres:15

# Initialize database
python setup_database.py
```

### **4. Local Kubernetes Setup (Free)**

```bash
# Option 1: Docker Desktop Kubernetes (FREE)
# Enable Kubernetes in Docker Desktop settings

# Option 2: Minikube (FREE)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start

# Test Kubernetes
kubectl get nodes
```

### **5. Local Monitoring Setup (Free)**

```bash
# Start Prometheus (FREE)
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Start Grafana (FREE)
docker run -d --name grafana \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana

# Access monitoring:
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

## 🛠️ Free Tool Setup

### **GitHub Actions (FREE CI/CD)**

**Setup:**
1. Create GitHub account (free)
2. Create organization: `platformdavid` (free)
3. Generate personal access token (free)

**Benefits:**
- ✅ **2000 minutes/month** for private repos
- ✅ **Unlimited minutes** for public repos
- ✅ **Unlimited repositories**
- ✅ **Industry standard** (used by Netflix, Spotify)
- ✅ **Integrated with GitHub**

```bash
# Test GitHub token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### **GitHub Container Registry (FREE)**

**Setup:**
- Automatically available with GitHub account
- No additional setup required

**Benefits:**
- ✅ **Unlimited storage** for public images
- ✅ **500MB/month** for private images
- ✅ **Integrated with GitHub Actions**
- ✅ **No authentication complexity**

### **SonarCloud (FREE Code Quality)**

**Setup:**
1. Go to [sonarcloud.io](https://sonarcloud.io)
2. Sign up with GitHub (free)
3. Create organization: `platformdavid`
4. Get API token

**Benefits:**
- ✅ **Free for public repositories**
- ✅ **Same features as SonarQube**
- ✅ **GitHub integration**
- ✅ **No server maintenance**

```bash
# Test SonarCloud
curl -u $SONARCLOUD_TOKEN: \
  https://sonarcloud.io/api/qualitygates/project_status
```

### **Local Prometheus + Grafana (FREE Monitoring)**

**Setup:**
```bash
# Create Prometheus config
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'platform-engineering'
    static_configs:
      - targets: ['localhost:8000']
EOF

# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d
```

**Benefits:**
- ✅ **Completely free**
- ✅ **No usage limits**
- ✅ **Full control**
- ✅ **Industry standard tools**

## 🧪 Testing the Free Platform

### **1. Create Service (FREE)**

```bash
# Start the API
uvicorn app.main:app --reload

# Create service from template
curl -X POST "http://localhost:8000/api/v1/services/from-template/fastapi-api" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-api",
    "team": "test-team",
    "environment": "dev",
    "description": "Test API service"
  }'
```

### **2. Provision Service (FREE)**

```bash
# Provision all components
curl -X POST "http://localhost:8000/api/v1/services/1/provision" \
  -H "Content-Type: application/json" \
  -d '{
    "provision_cicd": true,
    "provision_infrastructure": true,
    "provision_monitoring": true
  }'
```

### **3. What Gets Created (All FREE)**

**GitHub Actions Workflow:**
- ✅ Repository: `platformdavid/test-api`
- ✅ Workflow: `.github/workflows/ci-cd.yml`
- ✅ Triggers: Push to main, PRs
- ✅ Jobs: Test, Security, SonarCloud, Build, Deploy

**Local Infrastructure:**
- ✅ Terraform configs (local)
- ✅ Kubernetes manifests (local cluster)
- ✅ Docker images (GitHub Container Registry)

**Local Monitoring:**
- ✅ Prometheus targets
- ✅ Grafana dashboards
- ✅ Health checks

## 💰 Cost Breakdown: $0 Total

| **Component** | **Cost** | **Notes** |
|---------------|----------|-----------|
| **GitHub Actions** | $0 | 2000 min/month free |
| **GitHub Container Registry** | $0 | Unlimited public images |
| **Local Kubernetes** | $0 | Minikube/Docker Desktop |
| **Local PostgreSQL** | $0 | Docker container |
| **Local Prometheus** | $0 | Docker container |
| **Local Grafana** | $0 | Docker container |
| **SonarCloud** | $0 | Free for public repos |
| **AWS (Your account)** | $0 | Free tier for 12 months |
| **Total** | **$0** | **Completely free!** |

## 🎯 Why This Approach is Better for Your Test

### **1. Demonstrates Cost Optimization**
- Shows you understand **free tier strategies**
- Proves you can **minimize infrastructure costs**
- Demonstrates **resource efficiency**

### **2. Industry Standard Tools**
- **GitHub Actions**: Used by Netflix, Spotify, FanDuel
- **Local Kubernetes**: Same as production, just local
- **Prometheus/Grafana**: Industry standard monitoring
- **SonarCloud**: Enterprise-grade code quality

### **3. Real Platform Engineering**
- **Self-service provisioning**
- **Infrastructure as Code**
- **CI/CD automation**
- **Monitoring and observability**
- **Multi-team support**

### **4. Scalable Architecture**
- Easy to migrate to cloud later
- Same patterns as production
- No vendor lock-in
- Standard tooling

## 🚀 Production Migration Path

When you get the job, this easily scales to production:

```bash
# Replace local with cloud (same code!)
# Local Kubernetes → EKS/GKE
# Local PostgreSQL → RDS/Aurora
# Local Prometheus → Managed Prometheus
# GitHub Actions → Keep (it's free!)
# SonarCloud → Keep (it's free!)
```

## 📊 Free Tier Limits & Best Practices

### **GitHub Actions Limits:**
- **Public repos**: Unlimited minutes
- **Private repos**: 2000 minutes/month
- **Concurrent jobs**: 20 (free tier)

### **GitHub Container Registry Limits:**
- **Public images**: Unlimited storage
- **Private images**: 500MB/month
- **Bandwidth**: 1GB/month

### **AWS Free Tier (12 months):**
- **EC2**: 750 hours/month
- **S3**: 5GB storage
- **RDS**: 750 hours/month
- **Lambda**: 1M requests/month

### **Best Practices:**
1. **Use public repositories** for unlimited GitHub Actions
2. **Clean up unused resources** regularly
3. **Monitor usage** to stay within limits
4. **Use local development** when possible

## 🎉 Success Metrics

**Your test demonstrates:**
- ✅ **Cost optimization** (zero spend)
- ✅ **Industry standards** (GitHub Actions, Kubernetes)
- ✅ **Platform engineering** (self-service, automation)
- ✅ **Scalability** (easy cloud migration)
- ✅ **Best practices** (monitoring, testing, security)

**This is exactly what FanDuel's Platform Engineering team wants to see!** 🎯

---

**💡 Pro Tip:** Mention in your interview that you chose free tier tools to demonstrate cost optimization and that the same architecture easily scales to production with minimal changes. This shows you understand both **cost management** and **enterprise scalability** - key skills for platform engineers!
