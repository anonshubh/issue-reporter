from django.urls import path
from . import views

app_name = 'infolist'

urlpatterns=[
    path('',views.info_list_display_view,name='list'),
]