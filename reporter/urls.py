from django.urls import path
from . import views

app_name = 'reporter'

urlpatterns=[
    path('',views.index_view,name='index'),
    path('about-us/',views.about_view,name='about'),
    path('feed-back/',views.feedback_view,name='feed-back'),
    path('documentation/',views.documentation_view,name='documentation'),
    path('send-mail/',views.send_remainder_mail_view,name='mail'),

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
    path('voted-list/<int:id>/',views.voted_users,name='voted-users'),
    
    path('contact-list/',views.contactlist_list_view,name='contact-list'),
    path('contact-pending/',views.contactlist_cr_pending_list,name='contact-pending'),
    path('contact-add/',views.contactlist_add_view,name='contact-add'),
    path('contact-approve/<int:pk>/',views.contactlist_approve_view,name='contact-approve'),
    path('contact-delete/<int:pk>/',views.contactlist_delete_view,name='contact-delete'),

    #Vote API EndPoints
    path('update-vote/',views.vote_update_view,name='vote-update'),
    path('get-vote/',views.vote_get_view,name='vote-get'),
]