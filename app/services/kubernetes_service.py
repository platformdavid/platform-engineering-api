"""
Kubernetes service for managing containerized deployments.

This service generates and manages Kubernetes manifests for services.
"""

import yaml
import tempfile
import os
from typing import Dict, Any, List, Optional
import asyncio
import subprocess

from app.config import settings


class KubernetesService:
    """
    Service for managing Kubernetes deployments.
    
    Kubernetes is the industry standard for container orchestration,
    used by companies like FanDuel, Netflix, and Spotify.
    """
    
    def __init__(self):
        """Initialize Kubernetes service."""
        self.namespace = settings.k8s_namespace
        self.cluster_name = settings.k8s_cluster_name
        self.registry_url = settings.container_registry_url
    
    async def create_deployment(self, service_name: str, service_type: str, environment: str) -> Dict[str, Any]:
        """
        Create Kubernetes deployment for a service.
        
        Args:
            service_name: Name of the service
            service_type: Type of service (api, web, worker)
            environment: Environment (dev, staging, prod)
            
        Returns:
            Dict containing deployment information
        """
        # Generate Kubernetes manifests
        manifests = self._generate_manifests(service_name, service_type, environment)
        
        # Apply manifests to cluster
        result = await self._apply_manifests(manifests, service_name)
        
        return result
    
    async def delete_deployment(self, service_name: str, environment: str) -> Dict[str, Any]:
        """
        Delete Kubernetes deployment for a service.
        
        Args:
            service_name: Name of the service
            environment: Environment (dev, staging, prod)
            
        Returns:
            Dict containing deletion result
        """
        try:
            # Delete deployment
            delete_result = await asyncio.create_subprocess_exec(
                "kubectl", "delete", "deployment", f"{service_name}-{environment}",
                "-n", self.namespace,
                "--ignore-not-found=true"
            )
            await delete_result.communicate()
            
            # Delete service
            service_result = await asyncio.create_subprocess_exec(
                "kubectl", "delete", "service", f"{service_name}-{environment}",
                "-n", self.namespace,
                "--ignore-not-found=true"
            )
            await service_result.communicate()
            
            # Delete ingress if exists
            ingress_result = await asyncio.create_subprocess_exec(
                "kubectl", "delete", "ingress", f"{service_name}-{environment}",
                "-n", self.namespace,
                "--ignore-not-found=true"
            )
            await ingress_result.communicate()
            
            return {"status": "deleted", "message": "Kubernetes resources deleted successfully"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _generate_manifests(self, service_name: str, service_type: str, environment: str) -> List[Dict[str, Any]]:
        """
        Generate Kubernetes manifests for a service.
        
        Args:
            service_name: Name of the service
            service_type: Type of service
            environment: Environment
            
        Returns:
            List of Kubernetes manifests
        """
        manifests = []
        
        # Add namespace if it doesn't exist
        manifests.append(self._generate_namespace())
        
        # Add deployment
        manifests.append(self._generate_deployment(service_name, service_type, environment))
        
        # Add service
        manifests.append(self._generate_service(service_name, environment))
        
        # Add ingress for web services
        if service_type == "web":
            manifests.append(self._generate_ingress(service_name, environment))
        
        # Add ConfigMap for configuration
        manifests.append(self._generate_configmap(service_name, environment))
        
        # Add HorizontalPodAutoscaler for scaling
        manifests.append(self._generate_hpa(service_name, environment))
        
        return manifests
    
    def _generate_namespace(self) -> Dict[str, Any]:
        """Generate namespace manifest."""
        return {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": self.namespace,
                "labels": {
                    "name": self.namespace,
                    "managed-by": "platform-engineering"
                }
            }
        }
    
    def _generate_deployment(self, service_name: str, service_type: str, environment: str) -> Dict[str, Any]:
        """Generate deployment manifest."""
        # Base deployment configuration
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"{service_name}-{environment}",
                "namespace": self.namespace,
                "labels": {
                    "app": service_name,
                    "environment": environment,
                    "managed-by": "platform-engineering"
                }
            },
            "spec": {
                "replicas": 2,
                "selector": {
                    "matchLabels": {
                        "app": service_name,
                        "environment": environment
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": service_name,
                            "environment": environment
                        }
                    },
                    "spec": {
                        "containers": [],
                        "imagePullSecrets": [
                            {"name": "registry-secret"}
                        ]
                    }
                }
            }
        }
        
        # Add container based on service type
        if service_type == "api":
            deployment["spec"]["template"]["spec"]["containers"] = [
                {
                    "name": service_name,
                    "image": f"{self.registry_url}/fanduel/{service_name}:latest",
                    "ports": [
                        {"containerPort": 8000, "protocol": "TCP"}
                    ],
                    "env": [
                        {"name": "ENVIRONMENT", "value": environment},
                        {"name": "SERVICE_NAME", "value": service_name}
                    ],
                    "envFrom": [
                        {"configMapRef": {"name": f"{service_name}-{environment}-config"}}
                    ],
                    "resources": {
                        "requests": {
                            "cpu": "250m",
                            "memory": "512Mi"
                        },
                        "limits": {
                            "cpu": "500m",
                            "memory": "1Gi"
                        }
                    },
                    "livenessProbe": {
                        "httpGet": {
                            "path": "/health",
                            "port": 8000
                        },
                        "initialDelaySeconds": 30,
                        "periodSeconds": 10
                    },
                    "readinessProbe": {
                        "httpGet": {
                            "path": "/health",
                            "port": 8000
                        },
                        "initialDelaySeconds": 5,
                        "periodSeconds": 5
                    }
                }
            ]
        elif service_type == "web":
            deployment["spec"]["template"]["spec"]["containers"] = [
                {
                    "name": service_name,
                    "image": f"{self.registry_url}/fanduel/{service_name}:latest",
                    "ports": [
                        {"containerPort": 80, "protocol": "TCP"}
                    ],
                    "env": [
                        {"name": "ENVIRONMENT", "value": environment},
                        {"name": "SERVICE_NAME", "value": service_name}
                    ],
                    "resources": {
                        "requests": {
                            "cpu": "100m",
                            "memory": "128Mi"
                        },
                        "limits": {
                            "cpu": "200m",
                            "memory": "256Mi"
                        }
                    }
                }
            ]
        elif service_type == "worker":
            deployment["spec"]["template"]["spec"]["containers"] = [
                {
                    "name": f"{service_name}-worker",
                    "image": f"{self.registry_url}/fanduel/{service_name}-worker:latest",
                    "env": [
                        {"name": "ENVIRONMENT", "value": environment},
                        {"name": "SERVICE_NAME", "value": service_name}
                    ],
                    "envFrom": [
                        {"configMapRef": {"name": f"{service_name}-{environment}-config"}}
                    ],
                    "resources": {
                        "requests": {
                            "cpu": "500m",
                            "memory": "1Gi"
                        },
                        "limits": {
                            "cpu": "1000m",
                            "memory": "2Gi"
                        }
                    }
                }
            ]
        
        return deployment
    
    def _generate_service(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate service manifest."""
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"{service_name}-{environment}",
                "namespace": self.namespace,
                "labels": {
                    "app": service_name,
                    "environment": environment
                }
            },
            "spec": {
                "selector": {
                    "app": service_name,
                    "environment": environment
                },
                "ports": [
                    {
                        "name": "http",
                        "port": 80,
                        "targetPort": 8000,
                        "protocol": "TCP"
                    }
                ],
                "type": "ClusterIP"
            }
        }
    
    def _generate_ingress(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate ingress manifest for web services."""
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"{service_name}-{environment}",
                "namespace": self.namespace,
                "annotations": {
                    "kubernetes.io/ingress.class": "nginx",
                    "cert-manager.io/cluster-issuer": "letsencrypt-prod",
                    "nginx.ingress.kubernetes.io/ssl-redirect": "true"
                }
            },
            "spec": {
                "tls": [
                    {
                        "hosts": [f"{service_name}.{environment}.fanduel.com"],
                        "secretName": f"{service_name}-{environment}-tls"
                    }
                ],
                "rules": [
                    {
                        "host": f"{service_name}.{environment}.fanduel.com",
                        "http": {
                            "paths": [
                                {
                                    "path": "/",
                                    "pathType": "Prefix",
                                    "backend": {
                                        "service": {
                                            "name": f"{service_name}-{environment}",
                                            "port": {
                                                "number": 80
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    
    def _generate_configmap(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate ConfigMap for service configuration."""
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": f"{service_name}-{environment}-config",
                "namespace": self.namespace
            },
            "data": {
                "DATABASE_URL": f"postgresql://{service_name}:password@postgres-{environment}:5432/{service_name}",
                "REDIS_URL": f"redis://redis-{environment}:6379/0",
                "LOG_LEVEL": "INFO",
                "ENVIRONMENT": environment
            }
        }
    
    def _generate_hpa(self, service_name: str, environment: str) -> Dict[str, Any]:
        """Generate HorizontalPodAutoscaler for automatic scaling."""
        return {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {
                "name": f"{service_name}-{environment}-hpa",
                "namespace": self.namespace
            },
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": f"{service_name}-{environment}"
                },
                "minReplicas": 2,
                "maxReplicas": 10,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 70
                            }
                        }
                    },
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "memory",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": 80
                            }
                        }
                    }
                ]
            }
        }
    
    async def _apply_manifests(self, manifests: List[Dict[str, Any]], service_name: str) -> Dict[str, Any]:
        """Apply Kubernetes manifests to the cluster."""
        try:
            # Create temporary file with all manifests
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                for manifest in manifests:
                    yaml.dump(manifest, f, default_flow_style=False)
                    f.write("---\n")
                temp_file = f.name
            
            # Apply manifests using kubectl
            result = await asyncio.create_subprocess_exec(
                "kubectl", "apply", "-f", temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            # Clean up temporary file
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "message": "Kubernetes resources created successfully",
                    "output": stdout.decode()
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to apply Kubernetes manifests",
                    "error": stderr.decode()
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_deployment_status(self, service_name: str, environment: str) -> Dict[str, Any]:
        """
        Get deployment status from Kubernetes.
        
        Args:
            service_name: Name of the service
            environment: Environment
            
        Returns:
            Dict containing deployment status
        """
        try:
            # Get deployment status
            result = await asyncio.create_subprocess_exec(
                "kubectl", "get", "deployment", f"{service_name}-{environment}",
                "-n", self.namespace,
                "-o", "json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                import json
                deployment_info = json.loads(stdout.decode())
                return {
                    "status": "success",
                    "deployment": deployment_info
                }
            else:
                return {
                    "status": "not_found",
                    "message": "Deployment not found"
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
