from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from Users.models import User
from Activities.models import Sentence, Group, Pattern, Verb
from django.db.models import Q
from django.views.generic import ListView, TemplateView

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

class SearchView(TemplateView):
    template_name = 'search_form.html'


class SearchResultsView(ListView):
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return query

    def get_context_data(self, **kwargs):
        query_name = self.request.GET.get('q')
        query_body = self.request.GET.get('a')
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context.update({
            'sentences': Sentence.objects.all().filter(
                Q(sentencename__icontains=query_name)
            ),
            'verbs': Verb.objects.all().filter(
                Q(verbname__icontains=query_name)
            ),
            'groups': Group.objects.all().filter(
                Q(groupname__icontains=query_name)
            ),
            'patterns': Pattern.objects.all().filter(
                Q(patternname__icontains=query_name)
            ),
        })
        return context
