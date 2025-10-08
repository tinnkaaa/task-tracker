from django.urls import path
from .views import TaskListViews, TaskDetailView, TaskCreateView, task_complete, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path("tasks/", TaskListViews.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/complete/", task_complete, name="task-complete"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]