from django.urls import path
from . import views

app_name = 'infolist'

urlpatterns=[
    path('',views.info_list_display_view,name='list'),
    path('add-subject/',views.info_list_add_subject_view,name='add-subject'),
    path('delete-subject/<int:id>/',views.info_list_delete_subject_view,name='delete-subject'),
    path('add/',views.info_list_add_view,name='add-info'),
    path('pending/',views.info_list_pending_list_view,name='pending'),
]