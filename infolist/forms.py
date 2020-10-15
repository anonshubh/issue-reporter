from django import forms

from tinymce.widgets import TinyMCE
from .models import Subject,InfoList

class InfoListForm(forms.ModelForm):
    class Meta:
        model = InfoList
        fields = ['subject','title','content']
        widgets = {
            'content':TinyMCE(attrs={'cols': 80, 'rows': 15})
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject']