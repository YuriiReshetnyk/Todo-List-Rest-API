"""
URL mappings for the task API.
"""
from django.urls import include, path
from rest_framework import routers

from task import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'tags', views.TagViewSet)

app_name = 'task'

urlpatterns = [
    path('', include(router.urls)),

]
