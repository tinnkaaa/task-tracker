from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task, Comment, CommentLike
from .forms import TaskForm, CommentForm
from .mixins import UserTaskMixin, SuccessMessageMixin

class TaskListViews(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    ordering = ["-created_at"]
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")


class TaskDetailView(LoginRequiredMixin, UserTaskMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "💬 Коментар додано!")
            return redirect('task-detail', pk=self.object.pk)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")
    success_message = "✅ Задачу успішно створено!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "done" if form.cleaned_data.get("is_completed") else "todo"
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserTaskMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")
    success_message = "✏️ Задачу оновлено!"


class TaskDeleteView(LoginRequiredMixin, UserTaskMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("task-list")
    success_message = "🗑 Задачу видалено!"

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "tasks/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})

    def test_func(self):
        return self.get_object().author == self.request.user

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "tasks/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


@login_required(login_url='login')
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = "done" if form.cleaned_data.get("is_completed") else "todo"
            
            # Handle file upload
            if 'file' in request.FILES:
                task.file = request.FILES['file']
                print(f"File received: {task.file.name} ({task.file.size} bytes)")
            
            task.save()
            messages.success(request, "✅ Задачу успішно створено!")
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

@login_required
def toggle_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect("task-detail", pk=comment.task.pk)