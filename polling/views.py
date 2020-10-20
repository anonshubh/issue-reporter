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
    qs = Poll.objects.filter(active=True,department=request.user.info.department,join=request.user.info.join_year).order_by('-timestamp')
    return render(request,'polling/poll-list.html',{'object_list':qs})


@login_required
def polling_detail_view(request,id):
    object = get_object_or_404(Poll,pk=id)
    if(not object.active):
        raise PermissionDenied
    options = object.options.all()
    live_votes = object.result.all().first()
    if(not live_votes is None):
        live_votes = live_votes.voted_users.all().count()
    else:
        live_votes = 0
    return render(request,'polling/poll-detail.html',{"object":object,'options':options,'live_voted':live_votes})


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
            already_voted_user = UserPoll.objects.get(user=user,poll=poll_result)   
            voted_option = already_voted_user.option
            if(voted_option==option_count):
                messages.success(request,"Your Option has Been Submitted!")
                return redirect("polling:list")
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


@login_required
def poll_close_view(request,id):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    poll_obj = get_object_or_404(Poll,pk=id)
    poll_obj.active = False
    poll_obj.save()
    messages.info(request,"Poll has Been Closed!")
    return redirect("polling:list")


@login_required
def poll_delete_view(request,id):
    if(not request.user.info.is_cr):
        raise PermissionDenied
    poll_obj = get_object_or_404(Poll,pk=id)
    options = poll_obj.options.all()
    for i in options:
        i.delete()
    poll_obj.delete()
    messages.info(request,"Poll has Been Deleted!")
    return redirect("polling:list")


@login_required
def poll_results_list(request):
    qs = Poll.objects.filter(active=False,department=request.user.info.department,join=request.user.info.join_year).order_by('-updated')
    return render(request,'polling/poll-results-list.html',{'object_list':qs})


@login_required
def poll_result_detail(request,id):
    object = get_object_or_404(Poll,pk=id)
    options_obj = object.options.all()
    total_votes = 0
    for i in options_obj:
        try:
            temp = i.count.all().first().count
            total_votes+=temp
        except:
            continue
    options = []
    for i in options_obj:
        temp_list = {}
        opt_percent = 0.0
        opt_number = 0
        try:
            opt_percent = ((i.count.all().first().count)/total_votes)*100
            opt_number = i.count.all().first().count
        except:
            pass
        opt_text = i.text
        temp_list["percent"] = str(opt_percent)
        temp_list["number"] = opt_number
        temp_list["text"] = opt_text
        options.append(temp_list)
    return render(request,'polling/poll-result-detail.html',{'object':object,'options':options})