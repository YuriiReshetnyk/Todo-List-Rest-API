"""
Views for the task APIs.
"""
from rest_framework import (
    permissions,
    authentication,
    viewsets,
    mixins,
)

from task.serializers import (
    TaskSerializer,
)
from core.models import (
    Task,
)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)\
            .order_by('-due_date')
