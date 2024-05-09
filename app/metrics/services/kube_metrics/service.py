import logging
from typing import Any

from celery import Task

from app.database.repositories.kube_collected_data import IKubeCollectedDataRepository

# mocks
from app.metrics.services.kube_metrics.mocks import (
    namespaces_mock,
    deployments_mock,
    pods_mock,
    nodes_mock,
    pods_dynamic_mocked_metrics,
    nodes_dynamic_mocked_metrics
)


class KubeMetricsService:
    def __init__(
        self,
        kube_repository: IKubeCollectedDataRepository,
        kube_metrics_collection_task: Task,
    ) -> None:
        self._kube_metrics_collection_task = kube_metrics_collection_task
        self._kube_repository = kube_repository

        self._logger = logging.getLogger(__name__)

        # TODO: uncomment in production kubernetes cluster
        # config.load_incluster_config()
        # self._core_api = client.CoreV1Api()
        # self._apps_api = client.AppsV1Api()
        # self._custom_objects_api = client.CustomObjectsApi()
        # self._node_metrics = self._custom_objects_api.list_cluster_custom_object(
        #     group="metrics.k8s.io",
        #     version="v1beta1",
        #     plural="nodes"
        # )

    def get_mocked_namespaces(self):
        return namespaces_mock

    def get_mocked_deployments(self):
        return deployments_mock

    def get_mocked_pods(self):
        return pods_mock

    def get_mocked_nodes(self):
        return nodes_mock

    def _retrieve_mocked_node_metrics(self):
        return nodes_dynamic_mocked_metrics

    def _retrieve_mocked_pod_metrics(self):
        return pods_dynamic_mocked_metrics

    def retrieve_kube_dynamic_metrics(self):
        node_metrics = self._retrieve_mocked_node_metrics()
        pod_metrics = self._retrieve_mocked_pod_metrics()

        self.save_kube_dynamic_metrics(node_metrics, pod_metrics)

        self._kube_metrics_collection_task.apply_async(countdown=240, expires=240.01)
        return node_metrics, pod_metrics

    def save_kube_dynamic_metrics(self, node_metrics: dict[str, Any], pod_metrics: dict[str, Any]) -> None:
        self._kube_repository.save_kube_data(node_metrics, pod_metrics)

    def get_node_metrics(self):
        metrics = self._kube_repository.query_nodes_data()
        return metrics

    def get_pod_metrics(self):
        metrics = self._kube_repository.query_pods_data()
        return metrics

    # def get_node_metrics(self):
    #     node_metrics = self._custom_objects_api.list_cluster_custom_object(
    #         group="metrics.k8s.io",
    #         version="v1beta1",
    #         plural="nodes"
    #     )
    #     print("Node Metrics:")
    #     print(node_metrics)
    #     return node_metrics

    # def get_pod_metrics(self):
    #     pod_metrics = self._custom_objects_api.list_namespaced_custom_object(
    #         group="metrics.k8s.io",
    #         version="v1beta1",
    #         plural="pods",
    #         namespace="default"
    #     )
    #     print("Pod Metrics:")
    #     print(pod_metrics)
    #     return pod_metrics

    # def get_namespaces(self):
        # namespaces = self._core_api.list_namespace()
        # result = []
        # for ns in namespaces.items:
        #     ns_data = {
        #         "name": ns.metadata.name,
        #         "status": ns.status.phase,
        #         "created_at": ns.metadata.creation_timestamp,
        #         "labels": ns.metadata.labels,
        #         "annotations": ns.metadata.annotations
        #     }
        #     result.append(ns_data)
        # return result

    # def get_deployments(self):
        # deployments = self._apps_api.list_deployment_for_all_namespaces()
        # result = []
        # for deploy in deployments.items:
        #     deploy_data = {
        #         "name": deploy.metadata.name,
        #         "namespace": deploy.metadata.namespace,
        #         "replicas": deploy.spec.replicas,
        #         "available_replicas": deploy.status.available_replicas,
        #         "unavailable_replicas": deploy.status.unavailable_replicas,
        #         "labels": deploy.metadata.labels,
        #         "created_at": deploy.metadata.creation_timestamp,
        #         "conditions": [{"type": cond.type, "status": cond.status, "reason": cond.reason} for cond in
        #                        deploy.status.conditions],
        #         "selector": deploy.spec.selector.match_labels
        #     }
        #     result.append(deploy_data)
        # return result

    # def get_pods(self):
        # pods = self._core_api.list_pod_for_all_namespaces()
        # result = []
        # for pod in pods.items:
        #     pod_data = {
        #         "name": pod.metadata.name,
        #         "namespace": pod.metadata.namespace,
        #         "status": pod.status.phase,
        #         "node_name": pod.spec.node_name,
        #         "created_at": pod.metadata.creation_timestamp,
        #         "ip": pod.status.pod_ip,
        #         "containers": [
        #             {
        #                 "name": container.name,
        #                 "image": container.image,
        #                 "ready": container.ready,
        #                 "restart_count": container.restart_count,
        #                 "state": container.state.to_dict()
        #             } for container in pod.status.container_statuses
        #         ]
        #     }
        #     result.append(pod_data)
        # return result

    # def get_nodes(self):
        # nodes = self._core_api.list_node()
        # result = []
        # for node in nodes.items:
        #     conditions = {condition.type: condition.status for condition in node.status.conditions}
        #     node_data = {
        #         "name": node.metadata.name,
        #         "status": conditions,
        #         "roles": [label for label, value in node.metadata.labels.items() if
        #                   value == "node-role.kubernetes.io/master"],
        #         "ip_address": node.status.addresses[0].address,
        #         "os_arch": node.status.node_info.architecture,
        #         "os_image": node.status.node_info.os_image,
        #         "cpu_capacity": node.status.capacity.get("cpu"),
        #         "memory_capacity": node.status.capacity.get("memory"),
        #         "allocatable_cpu": node.status.allocatable.get("cpu"),
        #         "allocatable_memory": node.status.allocatable.get("memory"),
        #         "created_at": node.metadata.creation_timestamp,
        #         "taints": [{"key": taint.key, "effect": taint.effect, "value": taint.value} for taint in
        #                    node.spec.taints] if node.spec.taints else []
        #     }
        #     result.append(node_data)
        # return result

    def save_namespaces_data(self):
        pass
