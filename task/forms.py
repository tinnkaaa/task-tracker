from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    is_completed = forms.BooleanField(
        required=False,
        label='Виконано',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Explicitly define the file field with custom attributes
    file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png,.gif',
            'id': 'file-upload'
        }),
        help_text='Максимальний розмір файлу: 5MB'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'is_completed', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву задачі'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишіть задачу'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a custom ID to the file input for easier JavaScript targeting
        self.fields['file'].widget.attrs.update({
            'id': 'id_file_upload',
            'onchange': 'updateFileName(this)'
        })
        
    def clean_file(self):
        file = self.cleaned_data.get('file', None)
        if file:
            # Limit file size to 5MB
            max_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_size:
                raise forms.ValidationError('Файл занадто великий. Максимальний розмір: 5MB')
        return file

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control mb-3',
                'placeholder': 'Напишіть коментар...'
            }),
        }