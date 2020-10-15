from django.db import models
from profiles.models import UserInfo


class Subject(models.Model):
    subject = models.CharField(max_length=56)
    department = models.CharField(max_length=20,blank=True)
    year = models.CharField(max_length=4,blank=True)

    def __str__(self):
        return str(self.subject)


class InfoList(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()
    department = models.CharField(max_length=20,blank=True)
    year = models.CharField(max_length=4,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title[:30])
