from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


@login_required
def polling_list_view(request):
    pass
