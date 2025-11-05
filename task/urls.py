from django.urls import path
from .views import TaskListViews, TaskDetailView, TaskCreateView, task_complete, TaskUpdateView, TaskDeleteView, CommentUpdateView, CommentDeleteView, toggle_like

urlpatterns = [
    path("", TaskListViews.as_view(), name="task-list"),
    path("tasks/", TaskListViews.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path("comment/<int:pk>/like/", toggle_like, name="comment-like"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/complete/", task_complete, name="task-complete"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]