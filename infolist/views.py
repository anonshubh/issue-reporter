from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import InfoList,Subject
from .forms import InfoListForm,SubjectForm

@login_required
def info_list_display_view(request):
    subject = Subject.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    qs = InfoList.objects.filter(department=request.user.info.department,year=request.user.info.join_year)
    data = []
    for i in subject:
        objects = qs.filter(subject=i)
        data.append(object)
    return render(request,'infolist/list.html',{'object_list':data})