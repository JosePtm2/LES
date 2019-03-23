from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

# Create your views here.


@login_required
def Home(request):
        return render(request,'main/home.html')
