from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import CustomUserCreationForm

class RegisterView(FormView):
    template_name = "auth_system/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)