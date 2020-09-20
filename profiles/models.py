from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Institute(models.Model):
    name = models.CharField(max_length =56)
    domain = models.CharField(max_length=56)

    def __str__(self):
        return self.domain

class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    is_cr = models.BooleanField(default=False)
    department = models.CharField(max_length=3)
    join_year = models.CharField(max_length=4)
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='allusers')
    registered_on = models.DateTimeField(auto_now_add=True)
    total_upvotes = models.IntegerField(default=0)
    total_downvotes = models.IntegerField(default=0)
    total_novotes = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-total_upvotes','-total_downvotes','-total_novotes']


@receiver(email_confirmed)
def user_info_creation(request,email_address,**kwargs):
    user = email_address.user
    email = user.email
    index = email.find('@')
    dot = email.find('.')
    domain = email[index+1:dot]
    if(domain == 'iiitdm'):
        inst_obj = Institute.objects.get(domain=domain)
        department = email[:3]
        year = email[3:5]
        year_ = "20"+year
    #Addition or selection of another Institute will be in 'else' clause 
    user_obj = UserInfo.objects.create(user=user,institute=inst_obj,department=department,join_year=year_)