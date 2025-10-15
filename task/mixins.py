from django.shortcuts import get_object_or_404
from django.contrib import messages

class UserTaskMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"))
        return obj

class SuccessMessageMixin:
    success_message = None
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response