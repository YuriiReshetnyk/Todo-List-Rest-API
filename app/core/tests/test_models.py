"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        user_details = {
            'email': 'test@example.com',
            'password': 'password123',
            'username': 'yura295',
            'phone_number': '+380999999999',
        }
        user = get_user_model().objects.create_user(**user_details)

        for field, value in user_details.items():
            if field == 'password':
                self.assertTrue(user.check_password(value))
            else:
                self.assertEqual(getattr(user, field), value)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['Test3@example.COM', 'Test3@example.com'],
            ['test4@EXAMPLE.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password='password123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'tset123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'password123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
