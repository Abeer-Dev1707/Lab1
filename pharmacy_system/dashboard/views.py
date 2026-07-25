from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    print(request.user)
    print(request.user.is_authenticated)
    return render(request, 'dashboard/home.html')