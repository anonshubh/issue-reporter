from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Report
from .forms import ReportForm
from profiles.models import UserInfo

def index_view(request):
    qs = []
    if request.user.is_authenticated:
        qs = Report.objects.filter(active=True,department=request.user.info.department)
    return render(request,'profiles/index.html',{'issue_list':qs})

@login_required
def archive_view(request):
    qs = Report.objects.filter(active=False,department=request.user.info.department)
    return render(request,'profiles/archived.html',{'issue_list':qs})

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
            instance.save()
            return redirect('reporter:index')
    return render(request,'profiles/issue-form.html',{'form':form})


def close_issue_view(request,pk):
    obj = get_object_or_404(Report,id=pk)
    if(obj.active):
        obj.active = False
    else:
        obj.active = True
    obj.save()
    return redirect('reporter:index')

