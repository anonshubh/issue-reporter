from django import forms

from .models import Report , ContactList , FeedBack

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title','content']

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


class ContactListForm(forms.ModelForm):
    class Meta:
        model = ContactList
        fields=['name','course','email','phone']


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = '__all__'