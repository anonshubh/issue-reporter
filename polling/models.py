from django.db import models

from profiles.models import UserInfo

class Option(models.Model):
    text = models.CharField(max_length=128)

    def __str__(self):
        return str(self.text[:20])

class Poll(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name='polluser',blank=True)
    statement = models.CharField(max_length=128)
    options = models.ManyToManyField(Option,blank=True,related_name='poll')
    department = models.CharField(max_length=20,blank=True)
    join = models.CharField(max_length=4,blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.statement[:20]} by {self.user}"
    

class OptionCount(models.Model):
    option = models.ForeignKey(Option,on_delete=models.CASCADE,related_name='count')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Count of {self.option}'



class PollResult(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='result')
    option_count = models.ManyToManyField(OptionCount)
    voted_users = models.ManyToManyField('UserPoll')

    def __str__(self):
        return f'Result of {self.poll}'

    
class UserPoll(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    poll = models.ForeignKey(PollResult,on_delete=models.CASCADE)
    option = models.ForeignKey(OptionCount,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} selected {self.option.option}'
