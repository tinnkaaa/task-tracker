from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Task

# Create your views here.
class TaskListViews(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    ordering = ["-created_at"]

