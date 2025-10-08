from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "TO DO"),
        ("in_progress", "IN PROGRESS"),
        ("done", "DONE")
    ]

    PRIORITY_CHOICES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH")
    ]
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="todo")
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default="low")
    is_completed = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.is_completed:
            self.status = "done"
        elif self.status == "done" and not self.is_completed:
            self.status = "todo"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
