from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['fname', 'lname', 'tel', 'city', 'messagek',]
