from django import forms
from .models import StudyTask
from django.utils import timezone

class StudyTaskForm(forms.ModelForm):
    class Meta:
        model = StudyTask
        fields = ['title', 'description', 'deadline']

        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        today = timezone.now().date()

        if deadline < today:
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline