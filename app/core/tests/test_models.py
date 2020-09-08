from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email="test@email.com", password="testpass"):
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_userCreateWithUsernameAndPassword(self):
        """Testing user creation"""
        username = "test@gmail.com"
        password = "test123"

        user = get_user_model().objects.create_user(
            username=username, password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
