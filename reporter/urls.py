from django.urls import path
from . import views

app_name = 'reporter'

urlpatterns=[
    path('',views.index_view,name='index'),
    path('report/',views.issue_form_view,name='issue-form'),
    path('close-stage/<int:pk>/',views.close_issue_view,name='close-issue'),
    path('close-delete/<int:pk>/',views.delete_resolve_line_view,name='resolve-line-delete'),
    path('resolved/',views.resolved_view,name='resolved'),
    path('resolve-issue/<int:pk>',views.resolve_issue_view,name='resolve-issue'),
    path('close/',views.close_view,name='close-stage'),
    path('delete/<int:pk>/',views.delete_issue_view,name='delete'),
    path('edit/<int:pk>/',views.edit_issue_view,name='edit'),
    
    #Vote API EndPoints
    path('update-vote/',views.vote_update_view,name='vote-update'),
    path('get-vote/',views.vote_get_view,name='vote-get'),
]