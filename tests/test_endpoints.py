import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.entrypoint import fastapi_app

client = TestClient(fastapi_app)


class TestEndpoints(unittest.TestCase):
    @patch('app.entrypoint.app.external_ping_service.ping')
    def test_get_icmp_pings(self, mock_ping):
        mock_ping.return_value = {"success": True}
        response = client.get("api/v1/external-ping")

        self.assertEqual(response.status_code, 404)

    @patch('app.entrypoint.app')
    def test_get_health_check_metrics(self, mock_app):
        mock_app.health_check_service.get_health_check_metrics.return_value = {"success": True}

        response = client.get("/api/v1/health-checks/123")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_get_health_checks(self, mock_app):
        mock_app.health_check_service.get_health_checks_list.return_value = [{"success": True}]

        response = client.get("/api/v1/health-checks")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_create_health_check(self, mock_app):
        mock_app.health_check_service.initialize_health_check.return_value = "123"

        response = client.post("/api/v1/health-checks")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_update_ping(self, mock_app):
        mock_app.health_check_service.update_health_check.return_value = "123"

        response = client.put("/api/v1/health-checks/123")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_cancel_ping(self, mock_app):
        mock_app.health_check_service.delete_health_check.return_value = "123"

        response = client.delete("/api/v1/health-checks/123")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_get_icmp_pings_error(self, mock_app):
        mock_app.external_ping_service.ping.return_value = {"error": "Host not specified"}

        response = client.get("api/v1/external-ping")

        self.assertEqual(response.status_code, 404)

    @patch('app.entrypoint.app')
    def test_get_health_check_metrics_error(self, mock_app):
        mock_app.health_check_service.get_health_check_metrics.return_value = {"error": "Not found"}

        response = client.get("/api/v1/health-checks/123")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_get_health_checks_error(self, mock_app):
        mock_app.health_check_service.get_health_checks_list.return_value = {"error": "Not found"}

        response = client.get("/api/v1/health-checks")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_create_health_check_error(self, mock_app):
        mock_app.health_check_service.initialize_health_check.return_value = {"error": "Not found"}

        response = client.post("/api/v1/health-checks")

        self.assertEqual(response.status_code, 401)

    @patch('app.entrypoint.app')
    def test_update_ping_error(self, mock_app):
        mock_app.health_check_service.update_health_check.return_value = {"error": "Not found"}

        response = client.put("/api/v1/health-checks/123")

        self.assertEqual(response.status_code, 401)
