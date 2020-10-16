from django import forms

from tinymce.widgets import TinyMCE
from .models import Subject,InfoList

class InfoListForm(forms.ModelForm):
    def __init__(self,department,year,*args,**kwargs):
        super(InfoListForm,self).__init__(*args,**kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(department=department,year=year)

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