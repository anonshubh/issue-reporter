from .models import Report,ContactList
from polling.models import Poll

def pending_issue_list_context(request):
    pending=-1
    if request.user.is_authenticated:
        pending = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=False).count()
    return {"pending_issue_count":pending}


def resolved_issue_list_context(request):
    resolved=-1
    if request.user.is_authenticated:
        resolved = Report.objects.filter(active=False,department=request.user.info.department,year=request.user.info.join_year,resolved=True).count()
    return {"resolved_issue_count":resolved}


def pending_contact_list_context(request):
    pending=-1
    if request.user.is_authenticated:
        pending = ContactList.objects.filter(department=request.user.info.department,year=request.user.info.join_year,approved=False).count()
    return {"pending_contact_count":pending}


def live_polls_count_context(request):
    count = -1
    if request.user.is_authenticated:
        count = Poll.objects.filter(active=True,department=request.user.info.department,join=request.user.info.join_year).count()
    return {"live_polls_count":count}
