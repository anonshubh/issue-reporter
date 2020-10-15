from django.urls import path
from . import views

app_name = 'infolist'

urlpatterns=[
    path('',views.info_list_display_view,name='list'),
    path('add-subject/',views.info_list_add_subject_view,name='add-subject'),
]