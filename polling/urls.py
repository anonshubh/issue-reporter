from django.urls import path
from . import views

app_name = 'polling'

urlpatterns=[
    path('',views.polling_list_view,name='polling-list'),
]