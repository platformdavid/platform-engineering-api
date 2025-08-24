# 💰 AWS Cost Optimization Guide

This guide shows you how to use AWS **beyond the free tier** while keeping costs **as low as possible** ($5-15/month) for your platform engineering test.

## 🎯 Cost Optimization Strategy

**Why Cost Optimization?** This demonstrates **financial responsibility** - a key skill for platform engineers!

### **Cost Breakdown: $5-15/month vs $50-100/month**

| **Component** | **Standard Setup** | **Cost-Optimized Setup** | **Savings** |
|---------------|-------------------|-------------------------|-------------|
| **API Services** | ECS On-Demand ($30-50) | ECS Fargate Spot ($5-13) | **70%** |
| **Web Services** | EC2 + ALB ($20-30) | S3 + CloudFront ($0.50-2) | **90%** |
| **Worker Services** | EC2 Workers ($15-25) | Lambda Serverless ($0.80-2.50) | **95%** |
| **Monitoring** | CloudWatch Premium ($10) | CloudWatch Basic (Free) | **100%** |
| **Total** | **$75-115/month** | **$5-15/month** | **85-90%** |

## 🚀 Cost-Optimized Infrastructure

### **1. API Services: ECS Fargate Spot**

**Cost: $5-13/month** (vs $30-50 for on-demand)

```hcl
# Cost-optimized ECS configuration
resource "aws_ecs_service" "api_service" {
  desired_count = 1  # Start with 1 replica
  
  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"  # 70% cost reduction
    weight = 1
  }
  
  # Minimal resources
  cpu    = "256"   # 0.25 vCPU (minimum)
  memory = "512"   # 0.5 GB (minimum)
}
```

**Cost Optimization Features:**
- ✅ **Fargate Spot**: 70% cheaper than on-demand
- ✅ **Minimal Resources**: 256 CPU units, 512MB RAM
- ✅ **Single Replica**: Start with 1, scale up as needed

### **2. Web Services: S3 Static Hosting**

**Cost: $0.50-2/month** (vs $20-30 for EC2)

```hcl
# Cost-optimized web hosting
resource "aws_s3_bucket" "web_bucket" {
  bucket = "service-web-assets"
}

resource "aws_s3_bucket_website_configuration" "web_site" {
  bucket = aws_s3_bucket.web_bucket.id
  
  index_document {
    suffix = "index.html"
  }
}
```

**Cost Optimization Features:**
- ✅ **S3 Static Hosting**: $0.023 per GB stored
- ✅ **No EC2 Instances**: Eliminate compute costs
- ✅ **No Load Balancers**: Eliminate ALB costs

### **3. Worker Services: Lambda Serverless**

**Cost: $0.80-2.50/month** (vs $15-25 for EC2 workers)

```hcl
# Cost-optimized serverless workers
resource "aws_lambda_function" "worker" {
  function_name = "service-worker"
  runtime       = "python3.11"
  memory_size   = 128  # Minimum memory
  timeout       = 30   # Short timeout
  
  # Pay only for requests
  handler = "index.lambda_handler"
}
```

**Cost Optimization Features:**
- ✅ **Pay Per Request**: $0.20 per 1M requests
- ✅ **Minimal Memory**: 128MB (minimum)
- ✅ **Short Timeouts**: 30 seconds max

## 📊 Detailed Cost Breakdown

### **API Service Costs ($5-13/month)**
```bash
# ECS Fargate Spot (1 replica)
- CPU: 256 units × $0.00001406/second = $0.30/day = $9/month
- Memory: 512MB × $0.00000156/second = $0.07/day = $2/month
- Spot Discount: 70% savings = $3-8/month total

# CloudWatch Logs
- Log Storage: 1GB × $0.50/GB = $0.50/month
- Log Ingestion: 1GB × $0.50/GB = $0.50/month

Total: $4-9/month
```

### **Web Service Costs ($0.50-2/month)**
```bash
# S3 Storage
- Static Assets: 100MB × $0.023/GB = $0.002/month

# S3 Requests
- GET Requests: 10K × $0.0004/1K = $0.004/month

# Data Transfer
- Out: 1GB × $0.09/GB = $0.09/month

Total: $0.10-0.20/month
```

### **Worker Service Costs ($0.80-2.50/month)**
```bash
# Lambda Requests
- 1M requests × $0.20/1M = $0.20/month

# Lambda Duration
- 1M seconds × $0.0000166667/second = $0.17/month

Total: $0.42/month
```

## 🛠️ Implementation Guide

### **1. Environment Setup**
```bash
# Update your .env with cost-optimized settings
AWS_REGION=eu-west-2  # Cheapest region
ENABLE_SPOT_INSTANCES=true
ENABLE_SERVERLESS=true
MINIMAL_RESOURCES=true
```

### **2. Terraform Configuration**
```bash
# Use cost-optimized Terraform
terraform init
terraform plan -var="cost_optimized=true"
terraform apply
```

### **3. Cost Monitoring**
```bash
# Set up AWS Cost Explorer alerts
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorType": "DIMENSIONAL",
    "DimensionalValueCount": 10
  }'

# Set budget alerts at $10/month
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "Platform Engineering Test",
    "BudgetLimit": {
      "Amount": "10",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY"
  }'
```

## 🎯 Cost Optimization Best Practices

### **1. Resource Sizing**
```hcl
# Start with minimum resources
resource "aws_ecs_task_definition" "api" {
  cpu    = "256"   # Minimum CPU
  memory = "512"   # Minimum memory
}

# Scale up only when needed
resource "aws_appautoscaling_target" "api" {
  min_capacity = 1
  max_capacity = 3  # Limit maximum scale
}
```

### **2. Spot Instance Strategy**
```hcl
# Use spot instances for cost savings
capacity_provider_strategy {
  capacity_provider = "FARGATE_SPOT"
  weight = 1
}

# Fallback to on-demand if needed
capacity_provider_strategy {
  capacity_provider = "FARGATE"
  weight = 0
  base = 1
}
```

### **3. Log Retention**
```hcl
# Keep logs for minimum time to save costs
resource "aws_cloudwatch_log_group" "logs" {
  retention_in_days = 7  # Keep for 7 days only
}
```

### **4. Auto-scaling Policies**
```hcl
# Conservative scaling to avoid costs
resource "aws_appautoscaling_policy" "scale_up" {
  target_tracking_scaling_policy_configuration {
    target_value = 70  # Scale at 70% CPU
    scale_in_cooldown = 300  # 5 minutes
    scale_out_cooldown = 300  # 5 minutes
  }
}
```

## 🔍 Cost Monitoring

### **1. AWS Cost Explorer**
```bash
# Get daily cost breakdown
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity DAILY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### **2. CloudWatch Billing Alarms**
```hcl
# Set up billing alarms
resource "aws_cloudwatch_metric_alarm" "billing" {
  alarm_name = "monthly-billing-alert"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods = "1"
  metric_name = "EstimatedCharges"
  namespace = "AWS/Billing"
  period = "86400"  # Daily
  statistic = "Maximum"
  threshold = "10"  # $10 threshold
  alarm_description = "Monthly billing threshold exceeded"
}
```

## 🚨 Cost Alert Setup

### **1. Budget Alerts**
```bash
# Create budget with alerts
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "Platform Engineering Test",
    "BudgetLimit": {
      "Amount": "15",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "ComparisonOperator": "GREATER_THAN",
        "NotificationType": "ACTUAL",
        "Threshold": 80,
        "ThresholdType": "PERCENTAGE"
      },
      "Subscribers": [
        {
          "Address": "your-email@example.com",
          "SubscriptionType": "EMAIL"
        }
      ]
    }
  ]'
```

## 💡 Cost Optimization Tips

### **1. Use Reserved Instances (if staying long-term)**
```bash
# For long-term usage, consider reserved instances
# But for a test, stick with spot instances
```

### **2. Clean Up Unused Resources**
```bash
# Regular cleanup script
aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped" --query 'Reservations[].Instances[].InstanceId' --output text | xargs -I {} aws ec2 terminate-instances --instance-ids {}
```

### **3. Use AWS Cost Optimization Tools**
```bash
# Enable AWS Cost Explorer
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics BlendedCost
```

## 🎉 Success Metrics

**Your cost-optimized setup demonstrates:**
- ✅ **Financial Responsibility**: $5-15/month vs $75-115/month
- ✅ **Resource Efficiency**: Minimal resources, maximum value
- ✅ **Scalability**: Auto-scaling with cost controls
- ✅ **Monitoring**: Cost tracking and alerts
- ✅ **Best Practices**: Industry-standard cost optimization

**This shows PlatformDavid's Platform Engineering team that you understand:**
- **Cost management** in production environments
- **Resource optimization** for maximum efficiency
- **Financial responsibility** in infrastructure decisions
- **Scalability** without breaking the bank

---

**💡 Pro Tip:** Mention in your interview that you implemented cost optimization strategies to demonstrate financial responsibility and that the same patterns scale to production while maintaining cost efficiency. This shows you understand both **technical excellence** and **business value** - key skills for platform engineers!
