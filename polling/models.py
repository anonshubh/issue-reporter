from django.db import models

from profiles.models import UserInfo

class Option(models.Model):
    text = models.CharField(max_length=56)

class Poll(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name='poll',blank=True)
    statement = models.CharField(max_length=128)
    options = models.ManyToManyField(Option,blank=True)
    department = models.CharField(max_length=20,blank=True)
    join = models.CharField(max_length=4,blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.content[:20]} by {self.user}"
    
