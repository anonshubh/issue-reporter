from django import forms

from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content']

class DeadlineForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control-sm'})
        }
        labels = {
            'deadline': ''
        }
