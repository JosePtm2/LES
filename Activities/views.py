from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Verb, Sentence, Group, Pattern, Resource, Artefact
from .forms import SentenceForm
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core import serializers
import json
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import Count

# Create your views here.


class AjaxableResponseMixin(object):
    
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
        
    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if(self.request.path[1:7] == 'create'):
            messages.success(self.request,f"")
        elif(self.request.path[1:7] == 'update'):
            messages.info(self.request,f"")
        if self.request.is_ajax():
            print(self.request.path)
            if(self.request.path == '/create_group/'):
                data = { 'local': 'groups/', 'pk': self.object.pk,}
            elif(self.request.path == '/create_pattern/'):
                data = { 'local': 'patterns/', 'pk': self.object.pk,}
            elif(self.request.path == '/create_verb/'):
                data = { 'local': 'verbs/', 'pk': self.object.pk,}
            elif(self.request.path == '/create_sentence/'):
                data = { 'local': 'sentences/', 'pk': self.object.pk,}
            elif(self.request.path == '/create_artefact/'):
                data = { 'local': 'artefacts/', 'pk': self.object.pk,}
            elif(self.request.path == '/create_resource/'):
                data = { 'local': 'resources/', 'pk': self.object.pk,}
            else:
                data = { 'local': '', 'pk': self.object.pk,}
            return JsonResponse(data)
        else:
            return response

#==========   VERB   ==========#
class ListVerb(ListView):
    model = Verb
    
    def get_context_data(self, **kwargs):
        context = super(ListVerb, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({'verbs': Verb.objects.filter(verbname__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'verbs':  Verb.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_verb(self.request)
        return super(ListVerb, self).get_queryset()
    
class DetailVerb(DetailView):
    model = Verb

class CreateVerb(AjaxableResponseMixin, CreateView):
    model = Verb
    fields = ['verbname', 'verbtype']
    success_url = reverse_lazy('verb_list')

    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        form.instance.save()

        q = Sentence.objects.filter(
            verb_sug__icontains=form.instance.verbname).filter(
                userid__organization=self.request.user.organization)

        print(q)
        print(form.instance)
        for sentence in q:
            sentence.verbid = form.instance
            sentence.save()

        return super(CreateVerb, self).form_valid(form)


class UpdateVerb(AjaxableResponseMixin, UpdateView):
    model = Verb
    fields = ['verbname', 'verbtype']
    success_url = reverse_lazy('verb_list')

class DeleteVerb(DeleteView):
    model = Verb
    success_url = reverse_lazy('verb_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteVerb, self).delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(DeleteVerb,self).get_context_data(**kwargs)
        context.update({'groups': Sentence.objects.all(), 'related': False})
        o = Verb.objects.all().filter(verbname=kwargs['object'])
        if Sentence.objects.select_related().filter(verbid=kwargs['object']).annotate(n_b=Count('verbid')).count() == 0:
            return context
        else:
            context.update({ 'related': True })
            return context
#==========   VERB   ==========#



    
    
#==========   SENTENCE   ==========#
class ListSentence(ListView):
    model = Sentence
    
    def get_context_data(self, **kwargs):
        context = super(ListSentence, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({ 'user_sentences': Sentence.objects.all().filter(userid=self.request.user).filter(sentencename__icontains=self.request.GET.get('search')),
            'sentences': Sentence.objects.filter(sentencename__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'user_sentences': Sentence.objects.all().filter(userid=self.request.user),
            'sentences':  Sentence.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_sentence(self.request)
        return super(ListSentence, self).get_queryset()
    
class DetailSentence(DetailView):
    model = Sentence

YEAR_CHOICES = ['2000', '2001', '2002', '2003', '2004', '2005', '2006',
                      '2007', '2008', '2009', '2010', '2011', '2012', '2013',
                      '2014', '2015', '2016', '2017', '2018', '2019']


class CreateSentence(AjaxableResponseMixin, CreateView):
    model = Sentence
    form_class = SentenceForm

    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
        if not form.instance.datarealizado:
            form.instance.DataRealizado = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateSentence, self).form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(CreateSentence, self).get_form(form_class)
        form.fields['datarealizado'] = forms.DateField(
            widget=forms.SelectDateWidget(years=YEAR_CHOICES))
        return form

    success_url = reverse_lazy('sentence_list')

class UpdateSentence(AjaxableResponseMixin, UpdateView):
    model = Sentence
    fields = ['sentencename', 'subject' , 'verbid', 'receiver', 'resourceid', 'artefactid', 'datarealizado']
    success_url = reverse_lazy('sentence_list')

class DeleteSentence(DeleteView):
    model = Sentence
    success_url = reverse_lazy('sentence_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, " ")
        return super(DeleteSentence, self).delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(DeleteSentence,self).get_context_data(**kwargs)
        context.update({'groups': Group.objects.all()})
        return context

#==========   SENTENCE   ==========#    


#==========   GROUP   ==========#
class ListGroup(ListView):
    model = Group
    
    def get_context_data(self, **kwargs):
        context = super(ListGroup, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({'groups': Group.objects.filter(groupname__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'groups':  Group.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_Group(self.request)
        return super(ListGroup, self).get_queryset()

class DetailGroup(DetailView):
    model = Group

class CreateGroup(AjaxableResponseMixin, CreateView):
    pkSentences = []
    model = Group
    fields = ['groupname', 'description']
    def get(self, request):
        if request.GET.getlist('id[]'):
            sent = []
            for x in request.GET.getlist('id[]'):
               sent.append(x)
               self.pkSentences.append(x)
            data = {'queryset' : serializers.serialize('json', Sentence.objects.all().filter(id__in=sent))}
            return JsonResponse(json.loads(data['queryset']), safe=False)
        return super().get(self,request)
    def form_valid(self, form):
        form.instance.creationdate = timezone.now()
        form.instance.userid = self.request.user
        form.instance.save()
        form.instance.sentences.set(Sentence.objects.all().filter(id__in=self.pkSentences))
        self.pkSentences.clear()
        return super(CreateGroup, self).form_valid(form)
    success_url = reverse_lazy('group_list')

class UpdateGroup(AjaxableResponseMixin, UpdateView):
    model = Group
    fields = ['groupname', 'description', 'sentences']
    success_url = reverse_lazy('group_list')

class DeleteGroup(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteGroup, self).delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(DeleteGroup,self).get_context_data(**kwargs)
        context.update({'groups': Pattern.objects.all()})
        return context
#==========   GROUP   ==========#





#==========   PATTERN   ==========#
class ListPattern(ListView):
    model = Pattern
    def get_context_data(self, **kwargs):
        context = super(ListPattern, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({ 'patterns': Pattern.objects.filter(patternname__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'patterns':  Pattern.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_Pattern(self.request)
        return super(ListPattern, self).get_queryset()

class DetailPattern(DetailView):
    model = Pattern

class CreatePattern(AjaxableResponseMixin, CreateView):
    pkGroup = []
    model = Pattern
    fields = ['patternname', 'description']
    def get(self, request):
        if request.GET.getlist('id[]'):
            group = []
            for x in request.GET.getlist('id[]'):
               group.append(x)
               self.pkGroup.append(x)
            data = {'queryset' : serializers.serialize('json', Group.objects.all().filter(id__in=group))}
            return JsonResponse(json.loads(data['queryset']), safe=False)
        return super().get(self,request)
    def form_valid(self, form):
        form.instance.data_creation = timezone.now()
        form.instance.userid = self.request.user
        form.instance.save()
        form.instance.groups.set(Group.objects.all().filter(id__in=self.pkGroup))
        self.pkGroup.clear()
        return super().form_valid(form)
    success_url = reverse_lazy('pattern_list')

class UpdatePattern(AjaxableResponseMixin, UpdateView):
    model = Pattern
    fields = ['patternname', 'description', 'groups']
    success_url = reverse_lazy('pattern_list')

class DeletePattern(DeleteView):
    model = Pattern
    success_url = reverse_lazy('pattern_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeletePattern, self).delete(request, *args, **kwargs)
#==========   PATTERN   ==========#    
    




#==========   RESOURCE   ==========#    
class ListResource(ListView):
    model = Resource
    def get_context_data(self, **kwargs):
        context = super(ListResource, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({ 'resources': Resource.objects.filter(resourcename__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'resources':  Resource.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_Resource(self.request)
        return super(ListResource, self).get_queryset()

class DetailResource(DetailView):
    model = Resource

class CreateResource(AjaxableResponseMixin, CreateView):
    model = Resource
    fields = ['resourcename']
    success_url = reverse_lazy('resource_list')    

    def form_valid(self, form):

        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        form.instance.save()
        q = Sentence.objects.filter(
            resource_sug__icontains=form.instance.resourcename).filter(
                userid__organization=self.request.user.organization)

        for sentence in q:
            sentence.resourceid = form.instance
            sentence.save()

        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateResource, self).form_valid(form)


class UpdateResource(AjaxableResponseMixin, UpdateView):
    model = Resource
    fields = ['resourcename']
    success_url = reverse_lazy('resource_list')

class DeleteResource(DeleteView):
    model = Resource
    success_url = reverse_lazy('resource_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteResource, self).delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(DeleteResource,self).get_context_data(**kwargs)
        context.update({'groups': Sentence.objects.all()})
        return context
#==========   RESOURCE   ==========#    
    




#==========   ARTEFACT   ==========#    
class ListArtefact(ListView):
    model = Artefact
    def get_context_data(self, **kwargs):
        context = super(ListArtefact, self).get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context.update({ 'artefacts': Artefact.objects.filter(artefactname__icontains=self.request.GET.get('search')).filter(userid__organization=self.request.user.organization)})
            return context
        context.update({
            'artefacts':  Artefact.objects.all().filter(userid__organization=self.request.user.organization)
        })
        return context

    def get_queryset(self):
        if 'search' in self.request.GET:
            return Search_Artefact(self.request)
        return super(ListArtefact, self).get_queryset()

class DetailArtefact(DetailView):
    model = Artefact

class CreateArtefact(AjaxableResponseMixin, CreateView):
    model = Artefact
    fields = ['artefactname']
    success_url = reverse_lazy('artefact_list')

    def form_valid(self, form):

        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        form.instance.save()
        q = Sentence.objects.filter(
            art_sug__icontains=form.instance.artefactname).filter(
                userid__organization=self.request.user.organization)

        print(form.instance)
        
        for sentence in q:
            sentence.artefactid = form.instance
            sentence.save()

        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateArtefact, self).form_valid(form)

class UpdateArtefact(AjaxableResponseMixin, UpdateView):
    model = Artefact
    fields = ['artefactname']
    success_url = reverse_lazy('artefact_list')

class DeleteArtefact(DeleteView):
    model = Artefact
    success_url = reverse_lazy('artefact_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteArtefact, self).delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(DeleteArtefact,self).get_context_data(**kwargs)
        context.update({'groups': Sentence.objects.all()})
        return context
#==========   ARTEFACT   ==========#

#=========== Search ===============#
def Search_verb(request):
    search_term=''
    search_term = request.GET['search']
    verbs = Verb.objects.filter(verbname__icontains=search_term)

    context = {"verbs": verbs,}
    return verbs

def Search_sentence(request):
    search_term=''
    search_term = request.GET['search']
    sentences = Sentence.objects.filter(sentencename__icontains=search_term)

    context = {"sentences": sentences,}

    return sentences

def Search_Artefact(request):
    search_term=''
    search_term = request.GET['search']
    artefact = Artefact.objects.filter(artefactname__icontains=search_term)

    context = {"artefact": artefact,}

    return artefact

def Search_Resource(request):
    search_term=''
    search_term = request.GET['search']
    resource = Resource.objects.filter(resourcename__icontains=search_term)

    context = {"resource": resource,}

    return resource

def Search_Group(request):
    search_term=''
    search_term = request.GET['search']
    group = Group.objects.filter(groupname__icontains=search_term)

    context = {"group": group,}

    return group

def Search_Pattern(request):
    search_term=''
    search_term = request.GET['search']
    pattern = Pattern.objects.filter(patternname__icontains=search_term)

    context = {"pattern": pattern,}

    return pattern
