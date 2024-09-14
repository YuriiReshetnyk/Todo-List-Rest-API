"""
Test for Django admin modifications.
"""
from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from rest_framework import status

from core import models


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self) -> None:
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
        )

    def test_user_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_task_list(self):
        """Test that tasks are listed on page."""
        task = models.Task.objects.create(
            user=self.user,
            description='Test description',
            due_date=timezone.make_aware(datetime(2025, 10, 9)),
        )
        url = reverse('admin:core_task_changelist')
        res = self.client.get(url)

        self.assertContains(res, task.user.email)
        self.assertContains(res, task.description)
        self.assertContains(res, task.priority)

    def test_edit_task_page(self):
        """Test the edit task page works."""
        task = models.Task.objects.create(
            user=self.user,
            description='Test description',
            due_date=timezone.make_aware(datetime(2025, 10, 9)),
        )
        url = reverse('admin:core_task_change', args=[task.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_task_page(self):
        """Test the create task page works."""
        url = reverse('admin:core_task_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tag_list(self):
        """Test that tags are listed on page."""
        tag = models.Tag.objects.create(
            user=self.user,
            name='Test tag',
        )
        url = reverse('admin:core_tag_changelist')
        res = self.client.get(url)

        self.assertContains(res, tag.user.email)
        self.assertContains(res, tag.name)

    def test_edit_tag_page(self):
        """Test the edit tag page works."""
        tag = models.Tag.objects.create(
            user=self.user,
            name='Test tag',
        )
        url = reverse('admin:core_tag_change', args=[tag.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_tag_page(self):
        """Test the create tag page works."""
        url = reverse('admin:core_tag_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
