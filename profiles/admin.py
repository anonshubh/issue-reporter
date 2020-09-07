from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User,Institute,UserInfo

admin.site.register(User, UserAdmin)
admin.site.register(Institute)
admin.site.register(UserInfo)

admin.site.unregister(Group)


