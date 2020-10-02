from django.contrib import admin

from .models import Poll,Option

admin.site.register(Poll)
admin.site.register(Option)
