import unittest
from app.metrics.entities import PingConfig
from app.metrics.entities.alert import Alert


class TestPingConfigEntity(unittest.TestCase):
    def setUp(self):
        self.ping_config = PingConfig(id='test_id', host='test_host', interval=1, is_paused=False, owner_id='test_owner')

    def test_ping_config_id(self):
        self.assertEqual(self.ping_config.id, 'test_id')

    def test_ping_config_host(self):
        self.assertEqual(self.ping_config.host, 'test_host')

    def test_ping_config_interval(self):
        self.assertEqual(self.ping_config.interval, 1)

    def test_ping_config_is_paused(self):
        self.assertEqual(self.ping_config.is_paused, False)

    def test_ping_config_owner_id(self):
        self.assertEqual(self.ping_config.owner_id, 'test_owner')


class TestAlertEntity(unittest.TestCase):
    def setUp(self):
        self.alert = Alert(id='test_id', email='test@test.com', for_=1, repeat_alert=2, alert_group=1, alert_type=1)

    def test_alert_id(self):
        self.assertEqual(self.alert.id, 'test_id')

    def test_alert_email(self):
        self.assertEqual(self.alert.email, 'test@test.com')

    def test_alert_for(self):
        self.assertEqual(self.alert.for_, 1)

    def test_alert_repeat_alert(self):
        self.assertEqual(self.alert.repeat_alert, 2)

    def test_alert_alert_group(self):
        self.assertEqual(self.alert.alert_group, 1)

    def test_alert_alert_type(self):
        self.assertEqual(self.alert.alert_type, 1)
