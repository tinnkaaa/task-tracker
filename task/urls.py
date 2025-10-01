from django.urls import path
from .views import TaskListViews

urlpatterns = [
    path("tasks/", TaskListViews.as_view(), name="task-list")
]