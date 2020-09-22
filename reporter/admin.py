from django.contrib import admin

from .models import Report,Vote,InformationList

admin.site.register(Report)
admin.site.register(Vote)
admin.site.register(InformationList)