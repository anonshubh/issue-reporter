from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        email = str(user.email)
        uname = ""
        for i in email:
            if(i=='@'):
                break
            uname+=i
        user.username = uname
        user.save()

        return user
