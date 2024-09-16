"""
Views for the task APIs.
"""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
)
from rest_framework import (
    permissions,
    authentication,
    viewsets,
    mixins,
)

from task.serializers import (
    TaskSerializer,
    TagSerializer,
)
from core.models import (
    Task,
    Tag,
)


def _params_to_ints(qs: str) -> list[int]:
    """Convert a list of strings to integers."""
    return [int(str_id) for str_id in qs.split(',')]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma seperated list of tag IDs to filter',
            )
        ]
    )
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
        tags = self.request.query_params.get('tags')

        queryset = self.queryset
        if tags:
            tag_ids = _params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-due_date')


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes',
            )
        ]
    )
)
class TagViewSet(viewsets.GenericViewSet,
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(task__isnull=False)
            
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
