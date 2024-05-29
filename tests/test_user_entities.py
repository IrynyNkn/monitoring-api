import unittest
from app.metrics.entities.user import User


class TestUserEntity(unittest.TestCase):
    def setUp(self):
        self.user = User(id='test_id', email='test@test.com', password_hash='hashed_password')

    def test_user_id(self):
        self.assertEqual(self.user.id, 'test_id')

    def test_user_email(self):
        self.assertEqual(self.user.email, 'test@test.com')

    def test_user_password_hash(self):
        self.assertEqual(self.user.password_hash, 'hashed_password')

    def test_user_without_password_hash(self):
        user_without_password = User(id='test_id', email='test@test.com')
        self.assertIsNone(user_without_password.password_hash)

    def test_user_with_empty_id(self):
        user_with_empty_id = User(id='', email='test@test.com', password_hash='hashed_password')
        self.assertEqual(user_with_empty_id.id, '')

    def test_user_with_empty_email(self):
        user_with_empty_email = User(id='test_id', email='', password_hash='hashed_password')
        self.assertEqual(user_with_empty_email.email, '')
