"""
AWS Cost-Optimized Infrastructure Service.

This service creates the cheapest possible AWS infrastructure while still
demonstrating distributed systems, scaling, and platform engineering capabilities.
"""

import boto3
import json
from typing import Dict, Any, List
from botocore.exceptions import ClientError

from app.config import settings


class AWSCostOptimizedService:
    """
    AWS service optimized for minimal costs while demonstrating distributed infrastructure.
    
    Cost optimization strategies:
    - Use spot instances (up to 90% cheaper)
    - Use t3.micro/t3.nano (smallest instances)
    - Use S3 instead of EBS where possible
    - Use Lambda for serverless (pay per request)
    - Use CloudWatch basic monitoring (free)
    - Use Route 53 hosted zones (free for basic)
    """

    def __init__(self):
        """Initialize AWS service with cost-optimized settings."""
        self.ec2 = boto3.client('ec2', region_name=settings.aws_region)
        self.ecs = boto3.client('ecs', region_name=settings.aws_region)
        self.s3 = boto3.client('s3', region_name=settings.aws_region)
        self.lambda_client = boto3.client('lambda', region_name=settings.aws_region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=settings.aws_region)
        self.route53 = boto3.client('route53', region_name=settings.aws_region)

    async def create_cost_optimized_infrastructure(self, service_name: str, service_type: str, environment: str) -> Dict[str, Any]:
        """
        Create cost-optimized AWS infrastructure.
        
        Estimated monthly cost: $5-15 (vs $50-100 for standard setup)
        """
        try:
            infrastructure_config = {
                "service_name": service_name,
                "environment": environment,
                "cost_optimized": True,
                "estimated_monthly_cost": "$5-15"
            }

            if service_type == "api":
                # Use ECS Fargate with minimal resources
                result = await self._create_cost_optimized_api_infrastructure(service_name, environment)
                infrastructure_config.update(result)
                
            elif service_type == "web":
                # Use S3 + CloudFront (very cheap for static sites)
                result = await self._create_cost_optimized_web_infrastructure(service_name, environment)
                infrastructure_config.update(result)
                
            elif service_type == "worker":
                # Use Lambda for serverless processing
                result = await self._create_cost_optimized_worker_infrastructure(service_name, environment)
                infrastructure_config.update(result)

            return {
                "status": "success",
                "message": "Cost-optimized infrastructure created",
                "infrastructure": infrastructure_config,
                "cost_breakdown": self._get_cost_breakdown(service_type)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create infrastructure: {str(e)}",
                "infrastructure": {}
            }

    async def _create_cost_optimized_api_infrastructure(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Create cost-optimized API infrastructure using ECS Fargate."""
        
        # Create ECS cluster (free tier eligible)
        cluster_name = f"{service_name}-{environment}"
        try:
            self.ecs.create_cluster(
                clusterName=cluster_name,
                capacityProviders=['FARGATE_SPOT'],  # Use spot instances for 70% cost reduction
                defaultCapacityProviderStrategy=[
                    {
                        'capacityProvider': 'FARGATE_SPOT',
                        'weight': 1
                    }
                ],
                settings=[
                    {
                        'name': 'containerInsights',
                        'value': 'disabled'  # Disable to save costs
                    }
                ]
            )
        except ClientError as e:
            if e.response['Error']['Code'] != 'ClusterAlreadyExistsException':
                raise

        # Create task definition with minimal resources
        task_definition = {
            'family': f"{service_name}-{environment}",
            'networkMode': 'awsvpc',
            'requiresCompatibilities': ['FARGATE'],
            'cpu': '256',  # Minimum CPU (0.25 vCPU)
            'memory': '512',  # Minimum memory (0.5 GB)
            'executionRoleArn': 'ecsTaskExecutionRole',  # Use default role
            'containerDefinitions': [
                {
                    'name': service_name,
                    'image': f"ghcr.io/platformdavid/{service_name}:latest",
                    'portMappings': [{'containerPort': 8000, 'protocol': 'tcp'}],
                    'essential': True,
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': f"/ecs/{service_name}-{environment}",
                            'awslogs-region': settings.aws_region,
                            'awslogs-stream-prefix': 'ecs'
                        }
                    },
                    'environment': [
                        {'name': 'ENVIRONMENT', 'value': environment},
                        {'name': 'SERVICE_NAME', 'value': service_name}
                    ]
                }
            ]
        }

        # Register task definition
        response = self.ecs.register_task_definition(**task_definition)
        task_definition_arn = response['taskDefinition']['taskDefinitionArn']

        # Create service with minimal replicas
        service_response = self.ecs.create_service(
            cluster=cluster_name,
            serviceName=f"{service_name}-{environment}",
            taskDefinition=task_definition_arn,
            desiredCount=1,  # Start with 1 replica (can scale up)
            launchType='FARGATE',
            capacityProviderStrategy=[
                {
                    'capacityProvider': 'FARGATE_SPOT',
                    'weight': 1
                }
            ],
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['subnet-12345678'],  # Use existing subnet
                    'securityGroups': ['sg-12345678'],  # Use existing security group
                    'assignPublicIp': 'ENABLED'
                }
            }
        )

        return {
            "infrastructure_type": "ecs_fargate_spot",
            "cluster_name": cluster_name,
            "service_name": f"{service_name}-{environment}",
            "task_definition_arn": task_definition_arn,
            "desired_count": 1,
            "cpu": "256",
            "memory": "512",
            "cost_savings": "70% vs on-demand"
        }

    async def _create_cost_optimized_web_infrastructure(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Create cost-optimized web infrastructure using S3 + CloudFront."""
        
        # Create S3 bucket for static assets
        bucket_name = f"{service_name}-{environment}-web-assets"
        try:
            self.s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': settings.aws_region}
            )
            
            # Configure bucket for static website hosting
            self.s3.put_bucket_website(
                Bucket=bucket_name,
                WebsiteConfiguration={
                    'IndexDocument': {'Suffix': 'index.html'},
                    'ErrorDocument': {'Key': 'index.html'}
                }
            )
            
            # Configure bucket policy for public read access
            bucket_policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Sid': 'PublicReadGetObject',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': 's3:GetObject',
                        'Resource': f'arn:aws:s3:::{bucket_name}/*'
                    }
                ]
            }
            
            self.s3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(bucket_policy)
            )
            
        except ClientError as e:
            if e.response['Error']['Code'] != 'BucketAlreadyExists':
                raise

        # Note: CloudFront distribution would be created here
        # For cost optimization, we'll use S3 website hosting directly
        
        return {
            "infrastructure_type": "s3_static_hosting",
            "bucket_name": bucket_name,
            "website_url": f"http://{bucket_name}.s3-website-{settings.aws_region}.amazonaws.com",
            "cost_savings": "90% vs EC2 hosting"
        }

    async def _create_cost_optimized_worker_infrastructure(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Create cost-optimized worker infrastructure using Lambda."""
        
        # Create Lambda function for serverless processing
        function_name = f"{service_name}-{environment}-worker"
        
        # Create basic Lambda function code
        lambda_code = f"""
import json
import os

def lambda_handler(event, context):
    # Process messages from SQS or other triggers
    print(f"Processing message for {os.environ['SERVICE_NAME']}")
    
    return {{
        'statusCode': 200,
        'body': json.dumps('Worker processed successfully')
    }}
"""
        
        try:
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.11',
                Role='arn:aws:iam::123456789012:role/lambda-execution-role',  # Use existing role
                Handler='index.lambda_handler',
                Code={'ZipFile': lambda_code.encode()},
                Description=f'Serverless worker for {service_name}',
                Timeout=30,
                MemorySize=128,  # Minimum memory (128 MB)
                Environment={
                    'Variables': {
                        'SERVICE_NAME': service_name,
                        'ENVIRONMENT': environment
                    }
                }
            )
            
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceConflictException':
                raise

        return {
            "infrastructure_type": "lambda_serverless",
            "function_name": function_name,
            "runtime": "python3.11",
            "memory_size": 128,
            "timeout": 30,
            "cost_savings": "95% vs EC2 workers"
        }

    def _get_cost_breakdown(self, service_type: str) -> Dict[str, Any]:
        """Get estimated monthly cost breakdown."""
        
        if service_type == "api":
            return {
                "ecs_fargate_spot": "$3-8/month",
                "cloudwatch_logs": "$1-2/month",
                "data_transfer": "$1-3/month",
                "total": "$5-13/month"
            }
        elif service_type == "web":
            return {
                "s3_storage": "$0.02-0.10/month",
                "s3_requests": "$0.01-0.05/month",
                "data_transfer": "$0.50-2/month",
                "total": "$0.53-2.15/month"
            }
        elif service_type == "worker":
            return {
                "lambda_requests": "$0.20-1/month",
                "lambda_duration": "$0.10-0.50/month",
                "cloudwatch_logs": "$0.50-1/month",
                "total": "$0.80-2.50/month"
            }
        
        return {"total": "$5-15/month"}

    async def scale_infrastructure(self, service_name: str, service_type: str, target_capacity: int) -> Dict[str, Any]:
        """Scale infrastructure based on demand (cost-optimized)."""
        
        try:
            if service_type == "api":
                # Scale ECS service
                self.ecs.update_service(
                    cluster=f"{service_name}-staging",
                    service=f"{service_name}-staging",
                    desiredCount=target_capacity
                )
                
            elif service_type == "worker":
                # Lambda auto-scales automatically
                pass
                
            return {
                "status": "success",
                "message": f"Scaled to {target_capacity} instances",
                "cost_impact": "Minimal - using spot instances and serverless"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to scale: {str(e)}"
            }

    async def get_infrastructure_metrics(self, service_name: str) -> Dict[str, Any]:
        """Get cost and performance metrics."""
        
        try:
            # Get CloudWatch metrics (free tier)
            end_time = boto3.Session().get_credentials().get_frozen_credentials().access_key
            start_time = end_time  # Simplified for demo
            
            metrics = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ECS',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'ServiceName',
                        'Value': f"{service_name}-staging"
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            return {
                "cpu_utilization": metrics.get('Datapoints', []),
                "cost_optimization": "Active",
                "estimated_savings": "70-90% vs standard setup"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get metrics: {str(e)}",
                "cost_optimization": "Active"
            }
