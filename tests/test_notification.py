import unittest
from unittest.mock import patch, MagicMock
from app.metrics.services.notifications.alerts import AlertsService
from app.routes.serializers import CreateAlert, AlertGroup, AlertType


class TestAlertsService(unittest.TestCase):
    @patch('app.metrics.services.notifications.alerts.AlertRepository')
    @patch('app.metrics.services.notifications.alerts.EmailNotifier')
    def setUp(self, mock_email_notifier, mock_alert_repository):
        self.alerts_service = AlertsService(mock_alert_repository, mock_email_notifier)

    def test_get_alerts_success(self):
        self.alerts_service._alert_repository.get_alerts.return_value = [{'id': 'test_id', 'email': 'test@test.com'}]

        result = self.alerts_service.get_alerts('test_user_id')

        self.assertEqual(result, [{'id': 'test_id', 'email': 'test@test.com'}])
        self.alerts_service._alert_repository.get_alerts.assert_called_once_with('test_user_id')

    def test_create_alert_success(self):
        self.alerts_service._alert_repository.create_alert.return_value = 'test_alert_id'

        cr = CreateAlert(email='test@test.com', for_=1, repeat_alert=2, alert_group=AlertGroup.ICMP_PING, alert_type=AlertType.HEALTH_CHECK_FAILED)
        result = self.alerts_service.create_alert(cr, 'test_user_id')

        self.assertEqual(result, 'test_alert_id')
        self.alerts_service._alert_repository.create_alert.assert_called_once()

    def test_update_alert_success(self):
        self.alerts_service._alert_repository.update_alert.return_value = 'test_alert_id'

        cr = CreateAlert(email='test@test.com', for_=1, repeat_alert=2, alert_group=AlertGroup.ICMP_PING, alert_type=AlertType.HEALTH_CHECK_FAILED)
        result = self.alerts_service.update_alert(cr, 'test_alert_id')

        self.assertEqual(result, 'test_alert_id')
        self.alerts_service._alert_repository.update_alert.assert_called_once()

    def test_delete_alert_success(self):
        self.alerts_service._alert_repository.delete_alert.return_value = 'test_alert_id'

        result = self.alerts_service.delete_alert('test_alert_id')

        self.assertEqual(result, 'test_alert_id')
        self.alerts_service._alert_repository.delete_alert.assert_called_once_with('test_alert_id')

    def test_send_alerts_success(self):
        self.alerts_service._notifier.send_email.return_value = None

        self.alerts_service.send_alert('test_ping_config', 'test_alert')
