from allauth.account.forms import SignupForm , LoginForm
from django import forms
from allauth.account.adapter import DefaultAccountAdapter 
from django.forms import ValidationError

from .models import Institute


class CustomLoginForm(LoginForm):
     def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs = {'placeholder': 'Rollno or Institute Email', 'autofocus': 'autofocus'}


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        email = str(user.email)
        email = email.lower()
        user.email = email
        index = email.find('@')
        dot = email.find('.')
        rollno = ""
        for i in email:
            if(i=='@'):
                break
            rollno+=i
        user.username = rollno
        user.first_name = self.cleaned_data['first_name'] 
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user

class RestrictEmailAdapter(DefaultAccountAdapter): 
    def clean_email(self, email): 
        RestrictedList = [] #List will include Restricted Emails 
        if email in RestrictedList: 
            raise ValidationError('You are restricted from registering!')
        index = email.find('@')
        dot = email.find('.')
        email = email.lower()
        rollno = email[0:9]
        if(len(rollno)!=9):
            raise ValidationError("Only Students Rollno Accepted!")
        branches = ("mdm","mfd","mpd","msm","coe","ced","edm","evd","esd")
        name_valid = email[0:3]
        year_valid = email[3:5]
        roll_valid = email[6:9]
        try:
            if(not name_valid in branches):
                raise ValidationError("Only Students Rollno Accepted!")
            year_valid=int(year_valid)
            roll_valid=int(roll_valid)
        except:
                raise ValidationError("Only Students Rollno Accepted!")
        domain = email[index+1:dot]
        b_or_i = email[5:6]
        b_or_i = b_or_i.lower()
        if(b_or_i!='i' and b_or_i!='b'):
            raise ValidationError("No Mtech/PhD supported, Contact Admin!")
        if(domain=='gmail'):
            raise ValidationError("Use only Official Institute Email ID!")
        if(email[index+1:]!='iiitdm.ac.in'):
            raise ValidationError("Re-Check Email Address!")
        domain_qs = Institute.objects.filter(domain=domain)
        if(domain_qs.exists()):
            domain_obj = domain_qs.first().domain
            if(domain == domain_obj):
                return email
        raise ValidationError("Currently, No Service available for this Institute, Contact Site Administrator!")
