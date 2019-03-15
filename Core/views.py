from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission


# Create your views here.


@login_required
def Home(request):
	return render(request, 'main/home.html',
	context={"permissions":Permission.objects.values('name').filter(group__user=request.user).distinct()})
