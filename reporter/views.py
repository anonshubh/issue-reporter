from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed,JsonResponse,HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json, datetime, pytz

from .models import Report , Vote, ContactList
from .forms import ReportForm , DeadlineForm, ContactListForm, FeedBackForm
from profiles.models import UserInfo

def index_view(request):
    qs = []
    form = DeadlineForm()
    if request.user.is_authenticated:
        qs = Report.objects.filter(active=True,department=request.user.info.department,year=request.user.info.join_year,resolved=False)
    return render(request,'reporter/index.html',{'issue_list':qs,'form':form})

def about_view(request):
    return render(request,'about.html')

@login_required
def resolved_view(request):
    qs = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=True).order_by('-updated')
    return render(request,'reporter/resolved.html',{'issue_list':qs})

@login_required
def close_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year):
        if(obj.active):
            obj.active = False
        else:
            obj.active = True
        obj.save()
        return redirect('reporter:close-stage')
    raise PermissionDenied


@login_required
def close_view(request):
    if(request.user.info.is_cr):
        if(request.method=='POST'):
            id_ = int(request.POST.get('id',None))
            resolve_message = request.POST.get('c-line',None)
            obj = Report.objects.get(id=id_)
            obj.cr_line = resolve_message
            obj.save()
        qs = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=False).order_by('-updated')
        return render(request,'reporter/closed.html',{'issue_list':qs})
    raise PermissionDenied


@login_required
def delete_resolve_line_view(request,pk):
    obj = Report.objects.get(id=pk)
    obj.cr_line = None
    obj.save()
    return redirect('reporter:close-stage')


@login_required
def issue_form_view(request):
    form = ReportForm()
    if request.method=='POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user_obj = UserInfo.objects.get(user=request.user)
            instance.user = user_obj
            instance.department = request.user.info.department
            instance.year = request.user.info.join_year
            instance.save()
            qs = UserInfo.objects.filter(department=request.user.info.department,join_year=request.user.info.join_year)
            for i in qs:
                (i.total_novotes)+=1
                i.save()
            return redirect('reporter:index')
    return render(request,'reporter/issue-form.html',{'form':form})

@login_required
def resolve_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year):
        obj.resolved = True
        obj.save()
        return redirect('reporter:resolved')
    raise PermissionDenied

@login_required
def delete_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if((obj.active == True and obj.resolved == False) or (request.user.info.is_cr)):
        if((request.user.info.is_cr and request.user.info.department == obj.department and request.user.info.join_year == obj.year) or (request.user == obj.user.user)):
            obj.delete()
            return redirect('reporter:index')
    raise PermissionDenied

@login_required
def edit_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(obj.active == True and obj.resolved == False):
        form = ReportForm(instance=obj)
        if(request.user==obj.user.user):
            if(request.method=='POST'):
                form = ReportForm(request.POST,instance=obj)
                if(form.is_valid()):
                    form.save()
                return redirect('reporter:index')
            return render(request,'reporter/edit-issue.html',{'form':form,'issue':obj})
    raise PermissionDenied

@login_required
def vote_update_view(request):
    if request.method == 'POST':
        data_ = json.loads(request.body)
        id_ = data_['id']
        type = data_['type']
        try:
            report_obj = Report.objects.get(id=id_)
            vote_obj,created = Vote.objects.get_or_create(user=request.user,issue=report_obj)
            userinfo_obj = UserInfo.objects.get(user=request.user)
        except:
            return HttpResponseServerError()
        if(report_obj.active == True and report_obj.resolved == False):
            if(type=='upvote'):
                (report_obj.upvotes)+=1
                (userinfo_obj.total_upvotes)+=1
                (userinfo_obj.total_novotes)-=1
                vote_obj.type = 1
            elif(type=='downvote'):
                (report_obj.downvotes)-=1
                (userinfo_obj.total_downvotes)-=1
                (userinfo_obj.total_novotes)-=1
                vote_obj.type = 0
            elif(type=='downvoted'):
                (report_obj.downvotes)+=1
                (userinfo_obj.total_downvotes)+=1
                (userinfo_obj.total_novotes)+=1
                vote_obj.type = -1
            elif(type=='upvoted'):
                (report_obj.upvotes)-=1
                (userinfo_obj.total_upvotes)-=1
                (userinfo_obj.total_novotes)+=1
                vote_obj.type = -1
            report_obj.save()
            vote_obj.save()
            userinfo_obj.save()
            return JsonResponse({'Success':'Voted'})
    return HttpResponseNotAllowed('POST')


@login_required
def vote_get_view(request):
    if request.method == 'POST':
        data_ = json.loads(request.body)
        id_ = data_['id']
        report_obj = Report.objects.get(id=id_)
        data = {}
        obj,created = Vote.objects.get_or_create(user=request.user,issue=report_obj)
        type_ = obj.type
        if(type_ == 1):
            data = {'type':'upvoted'}
        elif(type_ == 0):
            data = {'type':'downvoted'}
        elif(type_ == -1):
            data = {'type':'none'}
        return JsonResponse(data)
    return HttpResponseNotAllowed('POST')


@login_required
def voted_list_view(request):
    if(request.user.info.is_cr):
        department = request.user.info.department
        year = request.user.info.join_year
        qs = UserInfo.objects.filter(department=department,join_year=year)
        context = {}
        upvote_percent = 0.0
        downvote_percent = 0.0
        novote_percent = 0.0
        for i in qs:
            try:
                upvote_percent = (abs(i.total_upvotes)/(abs(i.total_upvotes)+abs(i.total_downvotes)+abs(i.total_novotes)))*100
            except ZeroDivisionError:
                upvote_percent = 0.0
            try:
                downvote_percent = ((abs(i.total_downvotes))/(abs(i.total_upvotes)+abs(i.total_downvotes)+abs(i.total_novotes)))*100
            except ZeroDivisionError:
                downvote_percent = 0.0
            try:
                novote_percent = ((abs(i.total_novotes))/(abs(i.total_upvotes)+abs(i.total_downvotes)+abs(i.total_novotes)))*100
            except ZeroDivisionError:
                novote_percent = 0.0
            context[i.user.username] = (
                {'upvote':round(upvote_percent,2),
                'downvote':round(downvote_percent,2),
                'novote':round(novote_percent,2)
                }
            )
        return render(request,'reporter/voted-list.html',{'object_list':context})
    raise PermissionDenied


@login_required
def deadline_add_view(request):
    id_ = int(request.POST.get('id',None))
    form = DeadlineForm(request.POST)
    if(form.is_valid()):
        deadline = form.cleaned_data['deadline']
        live = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        if((live.date()==deadline.date() and live.time()<deadline.time()) or(live.date()<deadline.date())):
            report_obj = get_object_or_404(Report,id=id_)
            if((report_obj.active == True and report_obj.resolved == False) or (request.user.info.is_cr)):
                if((request.user.info.is_cr and request.user.info.department == report_obj.department and request.user.info.join_year == report_obj.year)):
                    report_obj.deadline = deadline
                    report_obj.save()
        else:
            messages.error(request,'Deadline Must Be Higher than Current Time!')
    else:
        messages.error(request,'Invalid-Datetime')
    return redirect("reporter:index")


@login_required
def deadline_remove_view(request,pk):
    report_obj = get_object_or_404(Report,id=pk)
    if((report_obj.active == True and report_obj.resolved == False) or (request.user.info.is_cr)):
        if((request.user.info.is_cr and request.user.info.department == report_obj.department and request.user.info.join_year == report_obj.year)):
            report_obj.deadline = None
            report_obj.save()
    return redirect("reporter:index")


@login_required
def contactlist_list_view(request):
    user = request.user.info
    qs = ContactList.objects.filter(department=user.department,year=user.join_year,approved=True)
    return render(request,'reporter/contact-list.html',{'object_list':qs})


@login_required
def contactlist_add_view(request):
    form = ContactListForm()
    if(request.method=='POST'):
        form = ContactListForm(request.POST)
        if(form.is_valid()):
            user_obj = request.user.info
            instance = form.save(commit=False)
            instance.user = user_obj
            instance.department = user_obj.department
            instance.year = user_obj.join_year
            if(user_obj.is_cr):
                instance.approved = True
            instance.save()
            if(not user_obj.is_cr):
                messages.info(request,"Information will be Added, Once approved by CR!")
            else:
                messages.info(request,"Information Added!")
            return redirect('reporter:contact-list')
    return render(request,'reporter/contact-add.html',{'form':form})


@login_required
def contactlist_approve_view(request,pk):
    obj = get_object_or_404(ContactList,id=pk)
    if(request.user.info.is_cr):
        obj.approved = True
        obj.save()
        return redirect("reporter:contact-pending")
    raise PermissionDenied

@login_required
def contactlist_delete_view(request,pk):
    obj = get_object_or_404(ContactList,id=pk)
    if(request.user.info==obj.user or request.user.info.is_cr):
        obj.delete()
        return redirect("reporter:contact-list")
    raise PermissionDenied


@login_required
def contactlist_cr_pending_list(request):
    user = request.user.info
    qs = ContactList.objects.filter(department=user.department,year=user.join_year,approved=False)
    return render(request,'reporter/contact-pending.html',{'object_list':qs})


def feedback_view(request):
    form = FeedBackForm()
    if(request.method=="POST"):
        form = FeedBackForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.info(request,"Thank You!, Your Message is Submitted to Site Administrator")
            return redirect("reporter:index")
        else:
            messages.error(request,"Invalid Data!, Please Re-Fill the Form")
            return redirect("reporter:feed-back")
    return render(request,'reporter/feedback-form.html',{'form':form})


def documentation_view(request):
    return render(request,'documentation.html')


@login_required
def send_remainder_mail_view(request):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    if(request.user.username=='testuser'):
        messages.info(request,"Feature not Supported for Test User!")
        return redirect("reporter:index")
    class_list = []
    qs = UserInfo.objects.filter(department=request.user.info.department,join_year=request.user.info.join_year)
    for i in qs:
        class_list.append(i.user.email)
    try:
        send_mail(
        'Reminder',
        """Kindly Vote your Opinion!, if Done ignore this Mail.
            https://teamezi.herokuapp.com/
        """,
        settings.DEFAULT_FROM_EMAIL,
        class_list,
        fail_silently=False,
        )
        messages.success(request,"Mail has Been Sent!")
    except:
        messages.warning(request,"Per Day Limit is Exceeded!")
    return redirect("reporter:index")


@login_required
def voted_users(request,id):
    issue_obj = get_object_or_404(Report,pk=id)
    if(issue_obj.anonymized):
        raise PermissionDenied
    votes = Vote.objects.filter(issue=issue_obj).order_by('-type')
    return render(request,'reporter/voted-users.html',{'votes':votes,'issue':issue_obj})