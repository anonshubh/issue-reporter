from django import forms

from .models import Poll

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ['join','department','user','active','options']