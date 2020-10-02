from django.urls import path
from . import views

app_name = 'polling'

urlpatterns=[
    path('',views.polling_list_view,name='list'),
    path('new/',views.poll_create_view,name='create'),
    path('<int:id>/',views.polling_detail_view,name='detail'),
    path('submit/',views.poll_submit_view,name='submit'),
]