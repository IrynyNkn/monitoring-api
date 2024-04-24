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
