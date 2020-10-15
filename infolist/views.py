from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import InfoList,Subject
from .forms import InfoListForm,SubjectForm

@login_required
def info_list_display_view(request):
    subjects = Subject.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    qs = InfoList.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    data = []
    for i in subjects:
        objects = qs.filter(subject=i)
        data.append(object)
    return render(request,'infolist/list.html',{'object_list':data})

@login_required
def info_list_add_subject_view(request):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    form = SubjectForm()
    subjects = Subject.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    if request.method=='POST':
        form = SubjectForm(request.POST)
        if(form.is_valid()):
            subject = request.POST.get("subject")
            sub_obj,created = Subject.objects.get_or_create(department=request.user.info.department,year=request.user.info.join_year,subject=subject)
            if created:
                messages.success(request,"Subject Added!")
            else:
                messages.info(request,"Subject Already Exists!")
        else:
            messages.error(request,"Form is Invalid!")
        return redirect('infolist:add-subject')
    return render(request,'infolist/add-subject.html',{'form':form,'subjects':subjects})