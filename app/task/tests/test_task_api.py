"""
Tests for task API.
"""
from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    Task,
)
from task.serializers import (
    TaskSerializer,
)


TASK_URL = reverse('task:task-list')


def detail_url(task_id):
    """Create and return a detail task URL."""
    return reverse('task:task-detail', args=[task_id])


def create_task(user, **params):
    default = {
        'description': 'Task',
        'due_date': timezone.make_aware(datetime(2089, 4, 20))
    }
    default.update(params)

    return Task.objects.create(user=user, **default)


class PublicTaskApiTest(TestCase):
    """Tests unauthorized Api requests."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required when retrieving tasks."""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskApiTest(TestCase):
    """Tests authorized Api requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
            username='Jonny123',
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task_successful(self):
        """Test creating a task."""
        payload = {
            "description": 'Test task',
            "due_date": timezone.make_aware(datetime(2089, 4, 20))
        }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)

    def test_is_complete_set_false_when_create(self):
        """Test is_complete is allways set to False when creating a task."""
        payload = {
            "description": 'Test task',
            "due_date": timezone.make_aware(datetime(2089, 4, 20)),
            "is_complete": True
        }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data['id'])
        self.assertEqual(task.is_complete, False)

    def test_retrieve_list_of_tasks(self):
        """Test retrieving a list of tasks."""
        create_task(self.user)
        create_task(self.user)

        res = self.client.get(TASK_URL)

        tasks = Task.objects.all().order_by('-due_date')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_limited_to_user(self):
        """Test retrieving list of tasks
        limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            email="test2@example.com",
            password='password123',
            username='extra',
        )
        create_task(other_user)
        create_task(self.user)
        create_task(self.user)

        res = self.client.get(TASK_URL)

        tasks = Task.objects.filter(user=self.user)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_task_details(self):
        """Test getting task details."""
        task = create_task(self.user)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskSerializer(task)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test updating a part of task."""
        task = create_task(user=self.user,
                           description='Test1')

        payload = {'description': 'New description'}
        url = detail_url(task.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.description, payload['description'])

    def test_full_update(self):
        """Test full update of a task."""
        task = create_task(user=self.user,
                           description='Test123',
                           due_date=timezone.make_aware(datetime(2024, 12, 12)),
                           priority=2)

        payload = {
            'description': 'New description',
            'due_date': timezone.make_aware(datetime(2025, 1, 1)),
            'is_complete': True,
            'priority': 3
        }
        url = detail_url(task.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)

    def test_update_user_returns_error(self):
        """Test updating a user results in an error."""
        other_user = get_user_model().objects.create_user(
            email='test22@example.com',
            password='password123',
            username='Yurii228',
        )
        task = create_task(user=self.user)

        payload = {
            'user': other_user
        }
        url = detail_url(task.id)
        res = self.client.patch(url, payload)

        task.refresh_from_db()
        self.assertEqual(task.user, self.user)

    def test_delete_task(self):
        """Test deleting a task."""
        task = create_task(self.user)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_other_user_task_error(self):
        """Test deleting other user task results in an error."""
        other_user = get_user_model().objects.create_user(
            email="test123@example.com",
            password='password123',
        )
        task = create_task(user=other_user)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
