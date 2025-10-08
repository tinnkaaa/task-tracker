from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    is_completed = forms.BooleanField(
        required=False,
        label='Виконано',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву задачі'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишіть задачу'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }