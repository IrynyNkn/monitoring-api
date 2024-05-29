import unittest
from unittest.mock import patch

from app.metrics.services.icmp_ping.service import PingService
from app.metrics.entities import PingConfig


class TestPingService(unittest.TestCase):
    @patch('app.metrics.services.icmp_ping.service.IPingConfigRepository')
    @patch('app.metrics.services.icmp_ping.service.Task')
    @patch('app.metrics.services.icmp_ping.service.IPingCollectedDataRepository')
    @patch('app.metrics.services.icmp_ping.service.AlertsService')
    def setUp(self, mock_alerts_service, mock_metrics_repository, mock_task, mock_ping_repository):
        self.ping_service = PingService(mock_ping_repository, mock_task, mock_metrics_repository, mock_alerts_service)

    def test_ping_success(self):
        self.ping_service._ping_repository.get.return_value = PingConfig(host='test_host', interval=1, is_paused=False, owner_id='test_owner')
        self.ping_service._ping_task.apply_async.return_value = None
        self.ping_service._metrics_repository.save_ping_data.return_value = None

        self.ping_service.ping('test_ping_id')

        self.ping_service._ping_repository.get.assert_called_once_with('test_ping_id')
        self.ping_service._ping_task.apply_async.assert_called_once()

    def test_add_new_ping_success(self):
        self.ping_service._ping_repository.save.return_value = 'test_ping_id'
        self.ping_service._ping_task.delay.return_value = None

        result = self.ping_service.add_new_ping('test_host', 1, 'test_owner')

        self.assertEqual(result, 'test_ping_id')
        self.ping_service._ping_repository.save.assert_called_once()
        self.ping_service._ping_task.delay.assert_called_once()
