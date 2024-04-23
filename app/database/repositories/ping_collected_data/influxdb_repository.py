import influxdb_client
from icmplib import Host
from influxdb_client.client.write_api import SYNCHRONOUS


from app.settings import AppSettings
from app.database.repositories.ping_collected_data.interface import IPingCollectedDataRepository
from app.metrics.entities import ExtendedPingConfig


class PingCollectedDataRepository(IPingCollectedDataRepository):
    def __init__(self, influxdb: influxdb_client.InfluxDBClient, settings: AppSettings) -> None:
        self._influxdb = influxdb
        self._settings = settings

        self._writer = self._influxdb.write_api(write_options=SYNCHRONOUS)
        self._query_api = self._influxdb.query_api()

    def get_ping_metrics(self, ping_id: str):
        query = f'''
        from(bucket: "{self._settings.influxdb_bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "ping")
          |> filter(fn: (r) => r.id == "{ping_id}")
          |> filter(fn: (r) => r._field == "round_trip_time")
        '''
        result = self._query_api.query(org=self._settings.influxdb_org, query=query)

        return result

    def save_ping_data(self, ping_response: Host, entity: ExtendedPingConfig):
        status = "success" if ping_response.packets_received > 0 else "failed"
        p = (influxdb_client.Point("ping")
             .tag("id", entity.id)
             .tag("host", entity.host)
             .field("status", status)
             .field("round_trip_time", entity.round_trip_time))

        self._writer.write(bucket=self._settings.influxdb_bucket, org=self._settings.influxdb_org, record=p)

        return self


