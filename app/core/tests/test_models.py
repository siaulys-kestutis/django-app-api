from django.test import TestCase
from django.contrib.auth import get_user_model

from app.settings import AUTH_USER_MODEL
from core.models import User


class ModelTests(TestCase):

    def test_create_user_with_email_password(self):
        email = 'test@gmail.com'
        password = 'test123'
        # presumably we are using the Django default user model

        user = get_user_model().user_manager.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        email = 'test@GMAIL.COM'
        user = get_user_model().user_manager.create_user(email=email, password="somePassword")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # this test passes if the following command throws a ValueError
        with self.assertRaises(ValueError):
            get_user_model().user_manager.create_user(email=None, password='somePassword')

    def test_create_create_new_superuser(self):
        user = get_user_model().user_manager.create_super_user("somethin@gmail.com", 'test123')
        # is_superuser is part of PermissionsMixin object
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
