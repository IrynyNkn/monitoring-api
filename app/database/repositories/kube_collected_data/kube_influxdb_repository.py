import logging
from typing import Any
import json

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import TableList

from app.settings import AppSettings
from app.database.repositories.kube_collected_data.interface import IKubeCollectedDataRepository


class KubeCollectedDataRepository(IKubeCollectedDataRepository):
    def __init__(self, influxdb: influxdb_client.InfluxDBClient, settings: AppSettings):
        self._influxdb = influxdb
        self._settings = settings

        self._writer = self._influxdb.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._influxdb.query_api()

        self._logger = logging.getLogger(self.__class__.__name__)

    def _save_node_data(self, entity: dict[str, Any]) -> None:
        try:
            for node_d in entity["items"]:
                memory_kib = int(node_d["usage"]["memory"].replace('Ki', ''))
                cpu_cores = int(node_d["usage"]["cpu"].replace('n', '')) / 1e9

                p = (
                    influxdb_client.Point("kube_node_metrics")
                    .tag("name", node_d["metadata"]["name"])
                    .field("cpu", cpu_cores)
                    .field("cpu_unit", "cores")
                    .field("memory", memory_kib)
                    .field("memory_unit", "Ki")
                )

                self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)
            # print("saved node data to influxdb")
        except Exception as exc:
            self._logger.error("Caught error on saving node metrics to db", exc)

    def _save_pod_data(self, entity: dict[str, Any]):
        try:
            for pod_d in entity["items"]:
                for container_d in pod_d["containers"]:
                    memory_kib = int(container_d["usage"]["memory"].replace('Ki', ''))
                    cpu_cores = int(container_d["usage"]["cpu"].replace('n', '')) / 1e9

                    p = (
                        influxdb_client.Point("kube_pod_metrics")
                        .tag("name", pod_d["metadata"]["name"])
                        .tag("namespace", pod_d["metadata"]["namespace"])
                        .tag("container", container_d["name"])
                        .field("cpu", cpu_cores)
                        .field("cpu_unit", "cores")
                        .field("memory", memory_kib)
                        .field("memory_unit", "Ki")
                    )

                    self._writer.write(
                        bucket=self._settings.influxdb_bucket,
                        org=self._settings.influxdb_org,
                        record=p,
                    )
            print("saved pod data to influxdb")
        except Exception as exc:
            self._logger.error("Caught error on saving pod metrics to db", exc)

    def save_kube_data(self, node_data: dict[str, Any], pod_data: dict[str, Any]) -> None:
        self._save_node_data(node_data)
        self._save_pod_data(pod_data)

    def query_nodes_data(self):
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -12h)
          |> filter(fn: (r) => r._measurement == "kube_node_metrics")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
                time: int(v: uint(v: r._time)) / 1000000,
                name: r.name,
                cpu: r.cpu,
                memory: r.memory,
                cpu_unit: r.cpu_unit,
                memory_unit: r.memory_unit
            }}))
        '''

        nodes_metrics: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        metrics = json.loads(nodes_metrics.to_json())

        return {
            "kube_metrics": metrics,
        }

    def query_pods_data(self):
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -12h)
          |> filter(fn: (r) => r._measurement == "kube_pod_metrics")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
                time: int(v: uint(v: r._time)) / 1000000,
                name: r.name,
                cpu: r.cpu,
                memory: r.memory,
                cpu_unit: r.cpu_unit,
                memory_unit: r.memory_unit
            }}))
        '''

        pods_metrics: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        metrics = json.loads(pods_metrics.to_json())

        return {"pod_metrics": metrics}

    def query_container_data_by_name(self, container_name: str):
        print("container_name", container_name)
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -12h)
          |> filter(fn: (r) => r._measurement == "kube_pod_metrics" and r.container == "{container_name}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
                time: int(v: uint(v: r._time)) / 1000000,
                pod_name: r.name,
                cpu: r.cpu,
                memory: r.memory,
                cpu_unit: r.cpu_unit,
                memory_unit: r.memory_unit
            }}))
        '''
        container_metrics: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        metrics = json.loads(container_metrics.to_json())

        return {"container_metrics": metrics}
