"""
Tests for models.
"""
from datetime import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


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

    def test_create_task(self):
        """Test creating a task."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
        )
        task = models.Task.objects.create(
            user=user,
            description='Test task',
            due_date=timezone.make_aware(datetime(2025, 10, 9)),
            priority=1,
        )
        self.assertEqual(str(task), task.description)

    def test_create_task_with_due_date_less_than_current_time_raise_error(self):
        """Test creating a task with due date with data
        earlier than current time raise ValueError."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
        )
        with self.assertRaises(ValidationError):
            models.Task.objects.create(
                user=user,
                description='Test task',
                due_date=timezone.make_aware(datetime(1889, 4, 20)),
            )

    def test_create_tag(self):
        """Test creating a tag."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
        )
        tag = models.Tag.objects.create(
            user=user,
            name='Tag1',
        )
        self.assertEqual(str(tag), tag.name)
