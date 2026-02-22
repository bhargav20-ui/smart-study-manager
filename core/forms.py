from django import forms
from .models import StudyTask
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudyTaskForm(forms.ModelForm):
    class Meta:
        model = StudyTask
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }