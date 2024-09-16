"""
Serializers for task APIs.
"""
from rest_framework import serializers

from core.models import (
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = ['id', 'created_at', 'description', 'is_complete',
                  'due_date', 'priority']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['is_complete'] = False
        validated_data['user'] = self.context['request'].user
        return Task.objects.create(**validated_data)
