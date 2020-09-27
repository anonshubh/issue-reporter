from django.contrib import admin

from .models import Report,Vote,ContactList,FeedBack

admin.site.register(Report)
admin.site.register(Vote)
admin.site.register(ContactList)
admin.site.register(FeedBack)