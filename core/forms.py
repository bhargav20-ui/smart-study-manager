from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import StudyTask


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class StudyTaskForm(forms.ModelForm):

    class Meta:
        model = StudyTask
        fields = ["title", "description", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"})
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        today = timezone.now().date()

        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline