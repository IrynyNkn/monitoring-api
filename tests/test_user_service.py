import unittest
from unittest.mock import patch, MagicMock
from app.metrics.services.accounts.user_service import UserService
from app.routes.serializers import RegisterUserData, LoginUserData


class TestUserService(unittest.TestCase):
    @patch('app.metrics.services.accounts.user_service.UserRepository')
    @patch('app.metrics.services.accounts.user_service.create_jwt_token')
    def setUp(self, mock_create_jwt_token, mock_user_repository):
        self.user_service = UserService(mock_user_repository)
        self.mock_create_jwt_token = mock_create_jwt_token

    @patch('app.metrics.services.accounts.user_service.create_jwt_token')
    def test_login_success(self, mock_create_jwt_token):
        self.user_service._user_repository.get_user_by_email.return_value = MagicMock(email='test@test.com', password_hash='hashed_password')
        self.user_service._validate_password_hash = lambda *args: True
        mock_create_jwt_token.return_value = 'test_token'

        result = self.user_service.login(LoginUserData(email='test@test.com', password='password'))

        self.assertEqual(result, {
            "user": {
                "id": self.user_service._user_repository.get_user_by_email.return_value.id,
                "email": 'test@test.com'
            },
            "token": 'test_token'
        })

    @patch('app.metrics.services.accounts.user_service.create_jwt_token')
    def test_register_success(self, mock_create_jwt_token):
        self.user_service._user_repository.create_user.return_value = MagicMock(email='test@test.com')
        mock_create_jwt_token.return_value = 'test_token'

        result = self.user_service.register(RegisterUserData(email='test@test.com', password='password', repeatPassword='password'))

        self.assertEqual(result, {
            "user": {
                "id": self.user_service._user_repository.create_user.return_value.id,
                "email": 'test@test.com'
            },
            "token": 'test_token'
        })

    def test_hash_password_no_error(self):
        self.user_service._hash_password('password')

    def test_validate_password_hash_no_error(self):
        assert not self.user_service._validate_password_hash('password', 'hashed_password')

    def test_validating_passwords(self):
        assert not self.user_service._validate_password_hash('password', 'invalid_hash')
