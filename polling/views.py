from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import Poll,Option
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
    if(request.method=='POST'):
        data = json.loads(request.body)
        obj = Poll.objects.create(
            user = request.user.info,
            statement = data['statement'],
            department= request.user.info.department,
            join = request.user.info.join_year
        )
        options = data['option']
        for i in options:
            new_option = Option.objects.create(text=i)
            obj.options.add(new_option)
        obj.save()
        messages.success(request, 'Poll is Created')
        return JsonResponse({"Success":"Created"},status=200)
    return render(request,'polling/poll-create.html',{"form":form})
