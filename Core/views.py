from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from Users.models import User
from Activities.models import Sentence, Group, Pattern, Verb

# Create your views here.


@login_required
def Home(request):
    return render(request,'main/home.html',
    context={"permissions":Permission.objects.values('name').filter(group__user=request.user).distinct(),
    "users":User.objects.all(),
    "sentences":Sentence.objects.all().filter(userid=request.user),
    "verbs":Verb.objects.all(),
    "groups":Group.objects.all().filter(userid=request.user),
    "patterns":Pattern.objects.all().filter(userid=request.user)})
