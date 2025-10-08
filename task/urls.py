from django.urls import path
from .views import TaskListViews, TaskDetailView, TaskCreateView, task_complete

urlpatterns = [
    path("tasks/", TaskListViews.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/complete/", task_complete, name="task-complete"),
]