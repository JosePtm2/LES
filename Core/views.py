from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def Home(request):
    if request.user.username == 'admin':
        return render(request, 'menuanalista.html')
    else:
        return render(request, 'menugestor.html')
