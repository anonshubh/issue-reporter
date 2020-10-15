from .models import InfoList

def pending_info_list_context(request):
    if request.user.is_superuser:
        return {}
    pending = -1
    if request.user.is_authenticated:
        pending = InfoList.objects.filter(department=request.user.info.department,year=request.user.info.join_year,approved=False).count()
    return {"pending_info_list":pending}