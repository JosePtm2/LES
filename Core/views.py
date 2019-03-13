from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def Home(request):
    return render(request, 'main/home.html')
