from django.urls import path
from . import views

app_name = 'polling'

urlpatterns=[
    path('',views.polling_list_view,name='list'),
    path('<int:id>/',views.polling_detail_view,name='detail'),
    path('submit/',views.poll_submit_view,name='submit'),
    path('close/<int:id>/',views.poll_close_view,name='close'),
    path('delete/<int:id>/',views.poll_delete_view,name='delete'),
    path('results/',views.poll_results_list,name='result-list'),
    path('result/<int:id>/',views.poll_result_detail,name='result-detail'),

    #API ENDPOINTS
    path('new/',views.poll_create_view,name='create'),
]