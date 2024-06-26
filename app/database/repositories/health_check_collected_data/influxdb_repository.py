from typing import Any, Dict
import json

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import TableList

from app.metrics.entities import ExtendedHCConfig
from app.settings import AppSettings
from app.database.repositories.health_check_collected_data import IHealthCheckCollectedDataRepo


class HealthCheckCollectedDataRepo(IHealthCheckCollectedDataRepo):
    def __init__(self, influxdb: influxdb_client.InfluxDBClient, settings: AppSettings) -> None:
        self._influxdb = influxdb
        self._settings = settings

        self._writer = self._influxdb.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._influxdb.query_api()

    def save_health_check_data(self, entity: ExtendedHCConfig):
        p = (influxdb_client.Point("health_check")
             .tag("id", entity.id)
             .tag("endpoint_url", entity.endpoint_url)
             .field("status", entity.status)
             .field("round_trip_time", entity.round_trip_time))

        self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)

        return self

    def get_health_check_metrics(self, health_check_id: str) -> Dict[str, Any]:
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -12h)
          |> filter(fn: (r) => r._measurement == "health_check")
          |> filter(fn: (r) => r.id == "{health_check_id}")
          |> filter(fn: (r) => r._field == "round_trip_time" or r._field == "status")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
              time: int(v: uint(v: r._time)) / 1000000,
              status: r.status,
              round_trip_time: r.round_trip_time
            }}))
        '''
        ping_tables: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        metrics = json.loads(ping_tables.to_json())

        metadata = self._get_health_check_metadata(health_check_id)
        metadata["health_check_id"] = health_check_id

        return {
            "metadata": metadata,
            "metrics": metrics
        }

    def _get_health_check_metadata(self, health_check_id: str):
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -12h)
          |> filter(fn: (r) => r._measurement == "health_check")
          |> filter(fn: (r) => r.id == "{health_check_id}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
              endpointUrl: r.endpoint_url,
              time: r._time, 
              status: r.status,
            }}))
          |> group()
          |> reduce(
              identity: {{
                endpointUrl: "",
                total: 0, 
                successful: 0, 
                failed: 0, 
                lastCheck: time(v: "1970-01-01T00:00:00Z"),
                firstCheck: now()
              }},
              fn: (r, accumulator) => ({{
                  total: accumulator.total + 1,
                  successful: accumulator.successful + (if r.status == 1 then 1 else 0),
                  failed: accumulator.failed + (if r.status == 1 then 0 else 1),
                  lastCheck: if r.time > accumulator.lastCheck then r.time else accumulator.lastCheck,
                  firstCheck: if r.time < accumulator.firstCheck then r.time else accumulator.firstCheck,
                  endpointUrl: r.endpointUrl
              }}))
          |> map(fn: (r) => ({{
              failed_checks: r.failed,
              success_rate: (r.successful / r.total) * 100,
              last_check_time: r.lastCheck,
              first_check_time: r.firstCheck,
              endpoint_url: r.endpointUrl,
              total_checks: r.total,
              successful_checks: r.successful
            }}))
        '''
        ping_tables: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        output = ping_tables.to_json()
        return json.loads(output)[0] if output != '[]' else {}
