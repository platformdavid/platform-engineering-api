"""
Terraform service for cost-optimized infrastructure provisioning.

This service generates Terraform configurations that create the cheapest possible
AWS infrastructure while still demonstrating distributed systems capabilities.
"""

import json
import subprocess
import os
from typing import Dict, Any, List
from pathlib import Path

from app.config import settings


class TerraformService:
    """
    Terraform service for cost-optimized infrastructure provisioning.
    
    Cost optimization strategies:
    - Use spot instances (up to 90% cheaper)
    - Use t3.micro/t3.nano (smallest instances)
    - Use S3 instead of EBS where possible
    - Use Lambda for serverless (pay per request)
    - Use CloudWatch basic monitoring (free)
    - Use Route 53 hosted zones (free for basic)
    """

    def __init__(self):
        """Initialize Terraform service with cost-optimized settings."""
        self.workspace_dir = settings.terraform_workspace_dir
        self.aws_region = settings.aws_region
        self.organization = settings.platform_organization

    async def create_infrastructure(self, service_name: str, service_type: str, environment: str) -> Dict[str, Any]:
        """
        Create cost-optimized infrastructure using Terraform.
        
        Estimated monthly cost: $5-15 (vs $50-100 for standard setup)
        """
        try:
            # Generate cost-optimized Terraform configuration
            terraform_config = self._generate_cost_optimized_config(service_name, service_type, environment)
            
            # Write Terraform files
            self._write_terraform_files(service_name, terraform_config)
            
            # Run Terraform
            result = await self._run_terraform(service_name, "apply")
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "Cost-optimized infrastructure created",
                    "outputs": result.get("outputs", {}),
                    "cost_breakdown": self._get_cost_breakdown(service_type),
                    "estimated_monthly_cost": "$5-15"
                }
            else:
                return {
                    "status": "error",
                    "message": result.get("error", "Terraform failed"),
                    "outputs": {}
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create infrastructure: {str(e)}",
                "outputs": {}
            }

    async def destroy_infrastructure(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Destroy infrastructure to stop costs."""
        try:
            result = await self._run_terraform(service_name, "destroy")
            return {
                "status": "success" if result["status"] == "success" else "error",
                "message": "Infrastructure destroyed" if result["status"] == "success" else result.get("error", "Failed to destroy"),
                "cost_savings": "100% - no ongoing charges"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to destroy infrastructure: {str(e)}"
            }

    def _generate_cost_optimized_config(self, service_name: str, service_type: str, environment: str) -> Dict[str, Any]:
        """Generate cost-optimized Terraform configuration."""
        
        config = {
            "terraform": {
                "required_version": ">= 1.0",
                "required_providers": {
                    "aws": {
                        "source": "hashicorp/aws",
                        "version": "~> 5.0"
                    }
                }
            },
            "provider": {
                "aws": {
                    "region": self.aws_region,
                    "default_tags": {
                        "tags": {
                            "Environment": environment,
                            "Service": service_name,
                            "ManagedBy": "platform-engineering",
                            "CostOptimized": "true"
                        }
                    }
                }
            },
            "locals": {
                "tags": {
                    "Environment": environment,
                    "Service": service_name,
                    "ManagedBy": "platform-engineering",
                    "CostOptimized": "true"
                }
            }
        }

        if service_type == "api":
            config["resource"] = self._generate_cost_optimized_api_resources(service_name, environment)
        elif service_type == "web":
            config["resource"] = self._generate_cost_optimized_web_resources(service_name, environment)
        elif service_type == "worker":
            config["resource"] = self._generate_cost_optimized_worker_resources(service_name, environment)

        return config

    def _generate_cost_optimized_api_resources(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate cost-optimized resources for API services."""
        return {
            "aws_ecs_cluster": {
                f"{service_name}_cluster": {
                    "name": f"{service_name}-{environment}",
                    "tags": "${local.tags}",
                    "setting": [
                        {
                            "name": "containerInsights",
                            "value": "disabled"  # Disable to save costs
                        }
                    ]
                }
            },
            "aws_ecs_task_definition": {
                f"{service_name}_task": {
                    "family": f"{service_name}-{environment}",
                    "network_mode": "awsvpc",
                    "requires_compatibilities": ["FARGATE"],
                    "cpu": "256",  # Minimum CPU (0.25 vCPU)
                    "memory": "512",  # Minimum memory (0.5 GB)
                    "execution_role_arn": "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
                    "container_definitions": json.dumps([
                        {
                            "name": service_name,
                            "image": f"ghcr.io/{self.organization}/{service_name}:latest",
                            "portMappings": [{"containerPort": 8000}],
                            "logConfiguration": {
                                "logDriver": "awslogs",
                                "options": {
                                    "awslogs-group": f"/ecs/{service_name}-{environment}",
                                    "awslogs-region": self.aws_region,
                                    "awslogs-stream-prefix": "ecs"
                                }
                            },
                            "environment": [
                                {"name": "ENVIRONMENT", "value": environment},
                                {"name": "SERVICE_NAME", "value": service_name}
                            ]
                        }
                    ]),
                    "tags": "${local.tags}"
                }
            },
            "aws_ecs_service": {
                f"{service_name}_service": {
                    "name": f"{service_name}-{environment}",
                    "cluster": f"${{aws_ecs_cluster.{service_name}_cluster.id}}",
                    "task_definition": f"${{aws_ecs_task_definition.{service_name}_task.arn}}",
                    "desired_count": 1,  # Start with 1 replica (can scale up)
                    "launch_type": "FARGATE",
                    "capacity_provider_strategy": [
                        {
                            "capacity_provider": "FARGATE_SPOT",  # Use spot instances for 70% cost reduction
                            "weight": 1
                        }
                    ],
                    "network_configuration": {
                        "subnets": ["subnet-12345678"],  # Use existing subnet
                        "security_groups": ["sg-12345678"],  # Use existing security group
                        "assign_public_ip": True
                    },
                    "tags": "${local.tags}"
                }
            },
            "aws_cloudwatch_log_group": {
                f"{service_name}_logs": {
                    "name": f"/ecs/{service_name}-{environment}",
                    "retention_in_days": 7,  # Keep logs for 7 days to save costs
                    "tags": "${local.tags}"
                }
            }
        }

    def _generate_cost_optimized_web_resources(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate cost-optimized resources for web services."""
        return {
            "aws_s3_bucket": {
                f"{service_name}_bucket": {
                    "bucket": f"{service_name}-{environment}-web-assets",
                    "tags": "${local.tags}"
                }
            },
            "aws_s3_bucket_website_configuration": {
                f"{service_name}_website": {
                    "bucket": f"${{aws_s3_bucket.{service_name}_bucket.id}}",
                    "index_document": {
                        "suffix": "index.html"
                    },
                    "error_document": {
                        "key": "index.html"
                    }
                }
            },
            "aws_s3_bucket_public_access_block": {
                f"{service_name}_public_access": {
                    "bucket": f"${{aws_s3_bucket.{service_name}_bucket.id}}",
                    "block_public_acls": False,
                    "block_public_policy": False,
                    "ignore_public_acls": False,
                    "restrict_public_buckets": False
                }
            },
            "aws_s3_bucket_policy": {
                f"{service_name}_policy": {
                    "bucket": f"${{aws_s3_bucket.{service_name}_bucket.id}}",
                    "policy": json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "PublicReadGetObject",
                                "Effect": "Allow",
                                "Principal": "*",
                                "Action": "s3:GetObject",
                                "Resource": f"${{aws_s3_bucket.{service_name}_bucket.arn}}/*"
                            }
                        ]
                    })
                }
            }
        }

    def _generate_cost_optimized_worker_resources(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate cost-optimized resources for worker services."""
        return {
            "aws_lambda_function": {
                f"{service_name}_worker": {
                    "filename": "lambda_function.zip",
                    "function_name": f"{service_name}-{environment}-worker",
                    "role": "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                    "handler": "index.lambda_handler",
                    "runtime": "python3.11",
                    "timeout": 30,
                    "memory_size": 128,  # Minimum memory (128 MB)
                    "environment": {
                        "variables": {
                            "SERVICE_NAME": service_name,
                            "ENVIRONMENT": environment
                        }
                    },
                    "tags": "${local.tags}"
                }
            },
            "aws_cloudwatch_log_group": {
                f"{service_name}_worker_logs": {
                    "name": f"/aws/lambda/{service_name}-{environment}-worker",
                    "retention_in_days": 7,  # Keep logs for 7 days to save costs
                    "tags": "${local.tags}"
                }
            }
        }

    def _write_terraform_files(self, service_name: str, config: Dict[str, Any]) -> None:
        """Write Terraform configuration files."""
        service_dir = Path(self.workspace_dir) / service_name
        service_dir.mkdir(parents=True, exist_ok=True)

        # Write main.tf
        main_tf = self._dict_to_hcl(config)
        with open(service_dir / "main.tf", "w") as f:
            f.write(main_tf)

        # Write variables.tf
        variables_tf = f"""
variable "environment" {{
  description = "Environment name"
  type        = string
  default     = "staging"
}}

variable "service_name" {{
  description = "Service name"
  type        = string
  default     = "{service_name}"
}}
"""
        with open(service_dir / "variables.tf", "w") as f:
            f.write(variables_tf)

        # Write outputs.tf
        outputs_tf = f"""
output "service_url" {{
  description = "Service URL"
  value       = "http://${{aws_ecs_service.{service_name}_service.name}}.platformdavid.com"
}}

output "estimated_monthly_cost" {{
  description = "Estimated monthly cost"
  value       = "$5-15"
}}

output "cost_optimization" {{
  description = "Cost optimization features"
  value       = "Spot instances, minimal resources, serverless where possible"
}}
"""
        with open(service_dir / "outputs.tf", "w") as f:
            f.write(outputs_tf)

    def _dict_to_hcl(self, data: Dict[str, Any]) -> str:
        """Convert dictionary to HCL format (simplified)."""
        # This is a simplified HCL conversion
        # In a real implementation, you'd use a proper HCL library
        return json.dumps(data, indent=2)

    async def _run_terraform(self, service_name: str, command: str) -> Dict[str, Any]:
        """Run Terraform command."""
        service_dir = Path(self.workspace_dir) / service_name
        
        try:
            # Set environment variables
            env = self._get_terraform_env()
            
            # Run terraform init
            if command == "apply":
                init_result = subprocess.run(
                    ["terraform", "init"],
                    cwd=service_dir,
                    env=env,
                    capture_output=True,
                    text=True
                )
                if init_result.returncode != 0:
                    return {
                        "status": "error",
                        "error": f"Terraform init failed: {init_result.stderr}"
                    }

            # Run terraform command
            result = subprocess.run(
                ["terraform", command, "-auto-approve"],
                cwd=service_dir,
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": result.stdout,
                    "outputs": self._parse_terraform_output(result.stdout)
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _get_terraform_env(self) -> Dict[str, str]:
        """Get environment variables for Terraform."""
        env = os.environ.copy()
        env.update({
            "AWS_ACCESS_KEY_ID": settings.aws_access_key_id,
            "AWS_SECRET_ACCESS_KEY": settings.aws_secret_access_key,
            "AWS_REGION": settings.aws_region
        })
        return env

    def _parse_terraform_output(self, output: str) -> Dict[str, Any]:
        """Parse Terraform output (simplified)."""
        # In a real implementation, you'd parse the actual Terraform output
        return {
            "service_url": "http://service.platformdavid.com",
            "estimated_monthly_cost": "$5-15",
            "cost_optimization": "Active"
        }

    def _get_cost_breakdown(self, service_type: str) -> Dict[str, Any]:
        """Get estimated monthly cost breakdown."""
        
        if service_type == "api":
            return {
                "ecs_fargate_spot": "$3-8/month",
                "cloudwatch_logs": "$1-2/month",
                "data_transfer": "$1-3/month",
                "total": "$5-13/month",
                "savings": "70% vs on-demand"
            }
        elif service_type == "web":
            return {
                "s3_storage": "$0.02-0.10/month",
                "s3_requests": "$0.01-0.05/month",
                "data_transfer": "$0.50-2/month",
                "total": "$0.53-2.15/month",
                "savings": "90% vs EC2 hosting"
            }
        elif service_type == "worker":
            return {
                "lambda_requests": "$0.20-1/month",
                "lambda_duration": "$0.10-0.50/month",
                "cloudwatch_logs": "$0.50-1/month",
                "total": "$0.80-2.50/month",
                "savings": "95% vs EC2 workers"
            }
        
        return {
            "total": "$5-15/month",
            "savings": "70-90% vs standard setup"
        }
