from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudyTask
from django.utils import timezone


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': ''
            })


class StudyTaskForm(forms.ModelForm):

    class Meta:
        model = StudyTask
        fields = ['title', 'description', 'deadline']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'deadline': forms.DateInput(attrs={
                'type':'date',
                'class':'form-control'
            })
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        today = timezone.now().date()

        if deadline and deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline