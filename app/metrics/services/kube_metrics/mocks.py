namespaces_mock = [
    {
        "name": "default",
        "status": "Active",
        "created_at": "2023-04-01T12:34:56Z",
        "labels": {
            "environment": "production"
        },
        "annotations": {
            "description": "Default namespace for the cluster"
        }
    },
    {
        "name": "development",
        "status": "Active",
        "created_at": "2023-03-25T15:45:30Z",
        "labels": {
            "environment": "development"
        },
        "annotations": {
            "description": "Namespace for development stage resources"
        }
    }
]

deployments_mock = [
    {
        "name": "frontend",
        "namespace": "production",
        "replicas": 3,
        "available_replicas": 3,
        "unavailable_replicas": 0,
        "labels": {
            "app": "web",
            "tier": "frontend"
        },
        "created_at": "2023-04-15T09:30:00Z",
        "conditions": [
            {
                "type": "Available",
                "status": "True",
                "reason": "MinimumReplicasAvailable"
            }
        ],
        "selector": {
            "app": "web",
            "tier": "frontend"
        }
    },
    {
        "name": "backend",
        "namespace": "production",
        "replicas": 2,
        "available_replicas": 1,
        "unavailable_replicas": 1,
        "labels": {
            "app": "api",
            "tier": "backend"
        },
        "created_at": "2023-04-10T11:20:00Z",
        "conditions": [
            {
                "type": "Progressing",
                "status": "True",
                "reason": "NewReplicaSetCreated"
            }
        ],
        "selector": {
            "app": "api",
            "tier": "backend"
        }
    }
]

pods_mock = [
    {
        "name": "web-frontend",
        "namespace": "default",
        "status": "Running",
        "node_name": "node1",
        "created_at": "2023-04-23T12:00:00Z",
        "ip": "10.244.1.2",
        "containers": [
            {
                "name": "nginx-container",
                "image": "nginx:latest",
                "ready": "true",
                "restart_count": 1,
                "state": {"running": {"started_at": "2023-04-23T12:01:00Z"}}
            }
        ]
    },
    {
        "name": "backend-api",
        "namespace": "default",
        "status": "Pending",
        "node_name": "node2",
        "created_at": "2023-04-23T11:59:00Z",
        "ip": "10.244.1.3",
        "containers": [
            {
                "name": "api-container",
                "image": "custom/api:1.2",
                "ready": "false",
                "restart_count": 0,
                "state": {"waiting": {"reason": "ContainerCreating"}}
            }
        ]
    }
]

nodes_mock = [
    {
        "name": "node1",
        "status": {
            "Ready": "True",
            "MemoryPressure": "False",
            "DiskPressure": "False",
            "PIDPressure": "False",
            "NetworkUnavailable": "False"
        },
        "roles": ["master"],
        "ip_address": "192.168.1.1",
        "os_arch": "amd64",
        "os_image": "Ubuntu 18.04.4 LTS",
        "cpu_capacity": "4",
        "memory_capacity": "16Gi",
        "allocatable_cpu": "3",
        "allocatable_memory": "15Gi",
        "created_at": "2022-01-01T12:00:00Z",
        "taints": [
            {
                "key": "node-role.kubernetes.io/master",
                "effect": "NoSchedule",
                "value": ""
            }
        ]
    },
    {
        "name": "node2",
        "status": {
            "Ready": "True",
            "MemoryPressure": "False",
            "DiskPressure": "False",
            "PIDPressure": "False",
            "NetworkUnavailable": "False"
        },
        "roles": ["worker"],
        "ip_address": "192.168.1.2",
        "os_arch": "amd64",
        "os_image": "Ubuntu 18.04.4 LTS",
        "cpu_capacity": "8",
        "memory_capacity": "32Gi",
        "allocatable_cpu": "7",
        "allocatable_memory": "30Gi",
        "created_at": "2022-01-02T12:00:00Z",
        "taints": []
    }
]

pods_dynamic_mocked_metrics = {
    "kind": "PodMetricsList",
    "apiVersion": "metrics.k8s.io/v1beta1",
    "metadata": {},
    "items": [
        {
            "metadata": {
                "name": "celery-worker-89b686b76-wcj5r",
                "namespace": "default",
                "creationTimestamp": "2024-04-24T12:39:56Z",
                "labels": {
                    "app": "celery-worker",
                    "pod-template-hash": "89b686b76"
                }
            },
            "timestamp": "2024-04-24T12:39:19Z",
            "window": "59.889s",
            "containers": [
                {
                    "name": "celery-worker",
                    "usage": {
                        "cpu": "967539n",
                        "memory": "278292Ki"
                    }
                }
            ]
        },
        {
            "metadata": {
                "name": "influxdb-5c4f76fb77-k9rwd",
                "namespace": "default",
                "creationTimestamp": "2024-04-24T12:39:56Z",
                "labels": {
                    "app": "influxdb",
                    "pod-template-hash": "5c4f76fb77"
                }
            },
            "timestamp": "2024-04-24T12:39:19Z",
            "window": "59.878s",
            "containers": [
                {
                    "name": "influxdb",
                    "usage": {
                        "cpu": "1209392n",
                        "memory": "46128Ki"
                    }
                }
            ]
        },
        {
            "metadata": {
                "name": "redis-7cf6f69fd-n75x4",
                "namespace": "default",
                "creationTimestamp": "2024-04-24T12:39:56Z",
                "labels": {
                    "app": "redis",
                    "pod-template-hash": "7cf6f69fd"
                }
            },
            "timestamp": "2024-04-24T12:39:19Z",
            "window": "59.943s",
            "containers": [
                {
                    "name": "redis",
                    "usage": {
                        "cpu": "1522429n",
                        "memory": "3216Ki"
                    }
                }
            ]
        }
    ]
}

nodes_dynamic_mocked_metrics = {
    "kind": "NodeMetricsList",
    "apiVersion": "metrics.k8s.io/v1beta1",
    "metadata": {},
    "items": [
        {
            "metadata": {
                "name": "minikube",
                "creationTimestamp": "2024-04-24T12:41:13Z",
                "labels": {
                    "beta.kubernetes.io/arch": "arm64",
                    "beta.kubernetes.io/os": "linux",
                    "kubernetes.io/arch": "arm64",
                    "kubernetes.io/hostname": "minikube",
                    "kubernetes.io/os": "linux",
                    "minikube.k8s.io/commit": "8220a6eb95f0a4d75f7f2d7b14cef975f050512d",
                    "minikube.k8s.io/name": "minikube",
                    "minikube.k8s.io/primary": "true",
                    "minikube.k8s.io/updated_at": "2024_02_07T12_27_18_0700",
                    "minikube.k8s.io/version": "v1.32.0",
                    "node-role.kubernetes.io/control-plane": "",
                    "node.kubernetes.io/exclude-from-external-load-balancers": ""
                }
            },
            "timestamp": "2024-04-24T12:40:16Z",
            "window": "1m0.996s",
            "usage": {
                "cpu": "231053413n",
                "memory": "1972348Ki"
            }
        }
    ]
}
