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
    path('voted-list/',views.voted_list_view,name='voted-list'),
    path('deadline-add/',views.deadline_add_view,name='add-deadline'),
    path('deadline-remove/<int:pk>',views.deadline_remove_view,name='remove-deadline'),
    
    path('info-list/',views.infolist_list_view,name='info-list'),
    path('info-pending/',views.infolist_cr_pending_list,name='info-pending'),
    path('info-add/',views.infolist_add_view,name='info-add'),
    path('info-approve/<int:pk>/',views.infolist_approve_view,name='info-approve'),
    path('info-delete/<int:pk>/',views.infolist_delete_view,name='info-delete'),
    #Vote API EndPoints
    path('update-vote/',views.vote_update_view,name='vote-update'),
    path('get-vote/',views.vote_get_view,name='vote-get'),
]