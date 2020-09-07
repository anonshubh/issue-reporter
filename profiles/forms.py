from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name') 
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        email = str(user.email)
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
