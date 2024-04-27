from typing import Any, Dict, List
import json

import influxdb_client
from icmplib import Host
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.flux_table import TableList


from app.settings import AppSettings
from app.database.repositories.ping_collected_data.interface import IPingCollectedDataRepository
from app.metrics.entities import ExtendedPingConfig


class PingCollectedDataRepository(IPingCollectedDataRepository):
    def __init__(self, influxdb: influxdb_client.InfluxDBClient, settings: AppSettings) -> None:
        self._influxdb = influxdb
        self._settings = settings

        self._writer = self._influxdb.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._influxdb.query_api()

    def get_ping_metrics(self, ping_id: str) -> Dict[str, Any]:
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "ping")
          |> filter(fn: (r) => r.id == "{ping_id}")
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

        metadata = self._get_ping_metadata(ping_id)
        metadata["ping_id"] = ping_id

        return {
            "metadata": metadata,
            "metrics": metrics,
        }

    def save_ping_data(self, ping_response: Host, entity: ExtendedPingConfig):
        status = "success" if ping_response.packets_received > 0 else "failed"
        p = (influxdb_client.Point("ping")
             .tag("id", entity.id)
             .tag("host", entity.host)
             .field("status", status)
             .field("round_trip_time", entity.round_trip_time))

        self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)

        return self

    def _get_ping_metadata(self, ping_id: str) -> Dict[str, Any]:
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "ping")
          |> filter(fn: (r) => r.id == "{ping_id}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> map(fn: (r) => ({{
              host: r.host,
              time: r._time, 
              status: r.status, 
              isSuccess: if r.status == "success" then 1 else 0,
              isFailure: if r.status == "failed" then 1 else 0
            }}))
          |> group()
          |> reduce(
              identity: {{
                host: "",
                total: 0, 
                successful: 0, 
                failed: 0, 
                lastCheck: time(v: "1970-01-01T00:00:00Z"),
                firstCheck: now()
              }},
              fn: (r, accumulator) => ({{
                  total: accumulator.total + 1,
                  successful: accumulator.successful + r.isSuccess,
                  failed: accumulator.failed + r.isFailure,
                  lastCheck: if r.time > accumulator.lastCheck then r.time else accumulator.lastCheck,
                  firstCheck: if r.time < accumulator.firstCheck then r.time else accumulator.firstCheck,
                  host: r.host
              }}))
          |> map(fn: (r) => ({{
              failed_checks: r.failed,
              success_rate: (r.successful / r.total) * 100,
              last_check_time: r.lastCheck,
              first_check_time: r.firstCheck,
              hostname: r.host,
              total_checks: r.total,
              successful_checks: r.successful
            }}))
        '''
        ping_tables: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
        output = ping_tables.to_json()
        return json.loads(output)[0] if output != '[]' else {}

    # def get_user_pings(self) -> List[Dict[str, Any]]:
    #     query = f'''
    #     from(bucket: "{self._settings.influxdb_bucket}")
    #     |> range(start: time(v: "1970-01-01T00:00:00Z"))
    #     |> filter(fn: (r) => r._measurement == "ping")
    #     |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    #     |> group(columns: ["id"])
    #     |> distinct(column: "host")
    #     '''
    #
    #     # | > map(fn: (r) = > ({{
    #     #     host: r.host,
    #     #     id: r.id,
    #     # }}))
    #
    #     # |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    #     ping_tables: TableList = self._query_api.query(org=self._settings.influxdb_org, query=query)
    #     output = ping_tables.to_json()
    #
    #     print("output", output)
    #     return json.loads(output)

