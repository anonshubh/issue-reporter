from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import InfoList,Subject
from .forms import InfoListForm,SubjectForm

@login_required
def info_list_display_view(request):
    subjects = Subject.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    qs = InfoList.objects.filter(department=request.user.info.department,year=request.user.info.join_year,approved=True)
    data = []
    for i in subjects:
        objects = qs.filter(subject=i)
        if(objects.count()==0):
            continue
        data.append([objects,i])
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


@login_required
def info_list_delete_subject_view(request,id):
    object = get_object_or_404(Subject,pk=id)
    object.delete()
    messages.success(request,"Subject has Been Deleted!")
    return redirect("infolist:add-subject")


@login_required
def info_list_add_view(request):
    form = InfoListForm(request.user.info.department,request.user.info.join_year)
    if(request.method=='POST'):
        form = InfoListForm(request.user.info.department,request.user.info.join_year,request.POST)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.user = request.user.info
            instance.department = request.user.info.department
            instance.year = request.user.info.join_year
            if(request.user.info.is_cr):
                instance.approved = True
                messages.info(request,"Info has been Added!")
            else:
                messages.info(request,"Info will be Added Once Approved by CR!")
            instance.save()
            return redirect('infolist:list')
    return render(request,'infolist/add-info.html',{'form':form})


@login_required
def info_list_pending_list_view(request):
    subjects = Subject.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    qs = InfoList.objects.filter(department=request.user.info.department,year=request.user.info.join_year,approved=False)
    data = []
    for i in subjects:
        objects = qs.filter(subject=i)
        if(objects.count()==0):
            continue
        data.append([objects,i])
    return render(request,'infolist/pending-list.html',{'object_list':data})


@login_required
def info_list_approve_view(request,id):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    obj = get_object_or_404(InfoList,pk=id)
    obj.approved = True
    obj.save()
    messages.info(request,"Info has Been Approved!")
    return redirect("infolist:pending")


@login_required
def info_list_delete_view(request,id):
    obj = get_object_or_404(InfoList,pk=id)
    if(request.user.info==obj.user or request.user.info.is_cr):
        obj.delete()
        return redirect("infolist:list")    
    raise PermissionDenied


@login_required
def meet_links_webpage(request):
    #User Permissions
    return render(request,"infolist/msm19.html")