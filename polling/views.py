from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .models import Poll
from .forms import PollForm

@login_required
def polling_list_view(request):
    qs = Poll.objects.filter(active=True,department=request.user.info.department,join=request.user.info.join_year)
    return render(request,'polling/poll-list.html',{'object_list':qs})


@login_required
def poll_create_view(request):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    form = PollForm()
    return render(request,'polling/poll-create.html',{"form":form})
