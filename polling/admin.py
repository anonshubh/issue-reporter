from django.contrib import admin

from .models import Poll,Option,OptionCount,PollResult,UserPoll

admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(PollResult)
admin.site.register(OptionCount)
admin.site.register(UserPoll)
