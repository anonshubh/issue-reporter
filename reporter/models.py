from django.db import models
from django.conf import settings

from profiles.models import UserInfo

class Report(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True)
    title = models.CharField('Subject',max_length=56)
    content = models.TextField('Issue')
    department = models.CharField(max_length=20,blank=True)
    year = models.CharField(max_length=4,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    resolved = models.BooleanField(default=False)
    cr_line = models.CharField(max_length=256,null=True,blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return f'By {self.user.user.username} ({self.content[:50]})'
    
    class Meta:
        ordering = ['-timestamp']


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    issue = models.ForeignKey(Report,related_name='votes',on_delete=models.CASCADE)
    type = models.IntegerField(default=-1)

    def __str__(self):
        return f"Vote By {self.user.username} On '{self.issue.content[:50]}'"



class InformationList(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=56)
    course = models.CharField(max_length=56)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    approved = models.BooleanField(default=False)
    department = models.CharField(max_length=20,blank=True)
    year = models.CharField(max_length=4,blank=True)

    def __str__(self):
        return str(self.name)


class FeedBack(models.Model):
    name = models.CharField(max_length=56)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"'{self.feedback[:10]}' By {self.name}"