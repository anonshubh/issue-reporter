from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Institute(models.Model):
    name = models.CharField(max_length =56)

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    is_cr = models.BooleanField(default=False)
    department = models.CharField(max_length=3)
    join_year = models.CharField(max_length=4)
    institute = models.ForeignKey(Institute,on_delete=models.CASCADE,related_name='allusers')

    def __str__(self):
        return self.user.username

