"""
Serializers for task APIs.
"""
from rest_framework import serializers

from core.models import (
    Task,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'created_at', 'description', 'is_complete',
                  'due_date', 'priority', 'tags']
        read_only_fields = ['id', 'created_at']

    def _get_or_create_tags(self, tags, task):
        """Handle creating or getting tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                name=tag.get('name'),
            )
            task.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a task."""
        tags = validated_data.pop('tags', [])

        validated_data['is_complete'] = False
        validated_data['user'] = self.context['request'].user
        task = Task.objects.create(**validated_data)

        if tags is not None:
            self._get_or_create_tags(tags, task)
        return task

    def update(self, instance, validated_data):
        """Update a task."""
        tags = validated_data.pop('tags', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags=tags, task=instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
