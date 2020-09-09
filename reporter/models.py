from django.db import models
from django.conf import settings

from profiles.models import UserInfo

class Report(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,blank=True)
    content = models.TextField('Issue')
    department = models.CharField(max_length=3,blank=True)
    year = models.CharField(max_length=4,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return f'By {self.user.user.username} ({self.content[:50]})'
    
    class Meta:
        ordering = ['-updated','-timestamp']


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    issue = models.ForeignKey(Report,related_name='votes',on_delete=models.CASCADE)
    type = models.IntegerField(default=-1)

    def __str__(self):
        return f"Vote By {self.user.username} On '{self.issue.content[:50]}'"
