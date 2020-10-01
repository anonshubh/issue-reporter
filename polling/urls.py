from django.urls import path
from . import views

app_name = 'polling'

urlpatterns=[
    path('',views.polling_list_view,name='list'),
    path('new/',views.poll_create_view,name='create'),
]