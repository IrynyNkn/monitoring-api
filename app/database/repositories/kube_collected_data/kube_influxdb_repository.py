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

    def save_kube_data(self):
        return
