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
        return f'By {self.user.user.username}'
    
    class Meta:
        ordering = ['-updated','-timestamp']
