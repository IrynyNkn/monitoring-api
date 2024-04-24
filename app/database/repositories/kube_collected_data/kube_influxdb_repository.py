from typing import Any

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from app.settings import AppSettings
from app.database.repositories.kube_collected_data.interface import IKubeCollectedDataRepository


class KubeCollectedDataRepository(IKubeCollectedDataRepository):
    def __init__(self, influxdb: influxdb_client.InfluxDBClient, settings: AppSettings):
        self._influxdb = influxdb
        self._settings = settings

        self._writer = self._influxdb.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._influxdb.query_api()

    def _save_node_data(self, entity: dict[str, Any]) -> None:
        try:
            for node_d in entity["items"]:
                p = (
                    influxdb_client.Point("kube_node_metrics")
                    .tag("name", node_d["metadata"]["name"])
                    .field("cpu", node_d["usage"]["cpu"])
                    .field("memory", node_d["usage"]["memory"])
                )

                self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)
        except Exception as exc:
            print("Caught error on saving node metrics to db", exc)

    def _save_pod_data(self, entity: dict[str, Any]):
        try:
            for pod_d in entity["items"]:
                for container_d in pod_d["containers"]:
                    p = (
                        influxdb_client.Point("kube_pod_metrics")
                        .tag("name", pod_d["metadata"]["name"])
                        .tag("namespace", pod_d["metadata"]["namespace"])
                        .tag("container", container_d["name"])
                        .field("cpu", container_d["usage"]["cpu"])
                        .field("memory", container_d["usage"]["memory"])
                    )

                    self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)
        except Exception as exc:
            print("Caught error on saving pod metrics to db", exc)

    def save_kube_data(self, node_data: dict[str, Any], pod_data: dict[str, Any]):
        self._save_node_data(node_data)
        self._save_pod_data(pod_data)
        return
