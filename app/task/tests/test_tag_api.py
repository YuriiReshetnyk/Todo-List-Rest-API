"""
Test tag APIs.
"""
from datetime import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import (
    Tag,
    Task,
)

from task.serializers import TagSerializer

TAG_URL = reverse('task:tag-list')


def detail_url(tag_id):
    """Create and return a detail tag URL."""
    return reverse('task:tag-detail', args=[tag_id])


def create_tag(user, name='Default name'):
    """Create and return a new tag."""
    return Tag.objects.create(user=user, name=name)


class PublicTagApiTest(TestCase):
    """Test unauthenticated tag APIs."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required."""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test authenticated tag APIs."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
            username='Test123',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        create_tag(user=self.user)
        create_tag(user=self.user)

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test the retrieved list of tags
        is limited to the authenticated user."""
        other_user = get_user_model().objects.create_user(
            email='OtherUser@example.com',
            password='password123',
            username='OtherName',
        )
        create_tag(user=other_user)
        create_tag(user=self.user)
        create_tag(user=self.user)

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = Tag.objects.filter(user=self.user).order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = create_tag(user=self.user, name='Test1')

        payload = {
            'name': 'New tag'
        }
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = create_tag(user=self.user)

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())

    def test_filter_tags_unique(self):
        """Test filtered tags return a unique list."""
        create_tag(user=self.user, name='Family')
        tag_work = create_tag(user=self.user, name='Work')

        task1 = Task.objects.create(
            user=self.user,
            description='Test task1',
            due_date=timezone.make_aware(datetime(2024, 12, 12))
        )
        task2 = Task.objects.create(
            user=self.user,
            description='Test task2',
            due_date=timezone.make_aware(datetime(2025, 12, 12))
        )
        task1.tags.add(tag_work)
        task2.tags.add(tag_work)

        res = self.client.get(TAG_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
