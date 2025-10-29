from django.db import models
from django.conf import settings
from auth_system.models import CustomUser

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
    file = models.FileField(upload_to='media_comments', null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.is_completed:
            self.status = "done"
        elif self.status == "done" and not self.is_completed:
            self.status = "todo"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='media_comments', null=True, blank=True)

    def __str__(self):
        return f"Коментар від {self.author} до {self.task.title}"

    @property
    def likes_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user} лайкнув {self.comment.id}"
