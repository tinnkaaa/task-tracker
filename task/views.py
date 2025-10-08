from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


# Create your views here.
class TaskListViews(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    ordering = ["-created_at"]
    login_url = reverse_lazy("admin:login")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    login_url = reverse_lazy("admin:login")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")
    login_url = reverse_lazy("admin:login")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.status = "done" if form.cleaned_data.get("is_completed") else "todo"
        task.save()
        return redirect("task-list")


@login_required(login_url='login')
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task-list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


@login_required(login_url='login')
def task_complete(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        task.is_completed = not task.is_completed
        task.status = "done" if task.is_completed else "todo"
        task.save()
    return redirect("task-list")