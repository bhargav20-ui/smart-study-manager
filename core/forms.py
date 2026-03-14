from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudyTask


# ---------------------------
# Registration Form
# ---------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove default help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        # apply bootstrap classes
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
# ---------------------------
# Study Task Form
# ---------------------------
class StudyTaskForm(forms.ModelForm):

    class Meta:
        model = StudyTask
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        today = timezone.now().date()

        # Safety check in case deadline is empty
        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline