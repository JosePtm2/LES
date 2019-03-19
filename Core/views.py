from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, Group
from Users.models import User

# Create your views here.


@login_required
def Home(request):
        return render(request,
                      'main/home.html',
                      context={"permissions":Permission.objects.values('name').filter(group__user=request.user).distinct(),
					  "users":User.objects.all(),
					  "groups":Group.objects.all()})
