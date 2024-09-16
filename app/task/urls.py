"""
URL mappings for the task API.
"""
from django.urls import include, path
from rest_framework import routers

from task import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

app_name = 'task'

urlpatterns = [
    path('', include(router.urls)),

]
