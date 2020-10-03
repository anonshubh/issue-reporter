from django.shortcuts import render,redirect ,get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import Poll,Option,PollResult,OptionCount,UserPoll
from .forms import PollForm

@login_required
def polling_list_view(request):
    qs = Poll.objects.filter(active=True,department=request.user.info.department,join=request.user.info.join_year)
    return render(request,'polling/poll-list.html',{'object_list':qs})


@login_required
def polling_detail_view(request,id):
    object = get_object_or_404(Poll,pk=id)
    options = object.options.all()
    return render(request,'polling/poll-detail.html',{"object":object,'options':options})


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


@login_required
def poll_submit_view(request):
    if(request.method=='POST'):
        poll_id = request.POST.get('poll',None)
        option_id = request.POST.get('option',None)
        poll_obj = get_object_or_404(Poll,pk=poll_id)
        option_obj = get_object_or_404(Option,pk=option_id)
        user = request.user.info

        option_count,created = OptionCount.objects.get_or_create(option=option_obj)
        poll_result,created0 = PollResult.objects.get_or_create(poll=poll_obj)

        available_options = poll_result.option_count
        if(not option_count in available_options.all()):
            available_options.add(option_count)
            poll_result.save()

        voted_users = poll_result.voted_users.all()
        voted_users_obj = []
        for i in voted_users:
            voted_users_obj.append(i.user)
        if(user in voted_users_obj):
            already_voted_user = UserPoll.objects.get(user=user)
            voted_option = already_voted_user.option
            voted_option.count-=1
            voted_option.save()
            already_voted_user.option = option_count
            already_voted_user.save()
        else:
            new_vote_user = UserPoll.objects.create(user=user,poll=poll_result,option=option_count)
            poll_result.voted_users.add(new_vote_user)
            poll_result.save()

        option_count.count+=1
        option_count.save()
        messages.success(request,"Your Option has Been Submitted!")
        return redirect("polling:list")
    raise PermissionDenied
