from allauth.account.forms import SignupForm

from .models import UserInfo , Institute

class CustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        email = str(user.email)
        rollno = ""
        for i in email:
            if(i=='@'):
                break
            rollno+=i
        user.username = rollno
        user.save()
        college = ""
        index = email.find('@')
        dot = email.find('.')
        college = email[index+1:dot]
        if(college == 'iiitdm'):
            inst_obj,created = Institute.objects.get_or_create(name='Indian Institute of Information Technology, Kancheepuram')
            department = rollno[:3]
            year = rollno[3:5]
            year_ = "20"+year
        user_obj = UserInfo.objects.create(user=user,institute=inst_obj,department=department,join_year=year_)

        return user
