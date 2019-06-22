from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Verb, Sentence, Group, Pattern, Resource, Artefact
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core import serializers
import json

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
            messages.success(self.request,f"a")
        elif(self.request.path[1:7] == 'update'):
            messages.info(self.request,f"a")
        if self.request.is_ajax():  
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

#==========   VERB   ==========#
class ListVerb(ListView):
    model = Verb

class DetailVerb(DetailView):
    model = Verb

class CreateVerb(AjaxableResponseMixin, CreateView):
    model = Verb
    fields = ['verbname', 'verbtype']
    success_url = reverse_lazy('verb_list')

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
#==========   VERB   ==========#



    
    
#==========   SENTENCE   ==========#
class ListSentence(ListView):
    model = Sentence
    
class DetailSentence(DetailView):
    model = Sentence
    
class CreateSentence(AjaxableResponseMixin, CreateView):
    model = Sentence
    fields = ['sentencename', 'subject' , 'verbid', 'receiver', 'resourceid', 'artefactid', 'datarealizado']
    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
        if not form.instance.datarealizado:
            form.instance.DataRealizado = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateSentence, self).form_valid(form)
    success_url = reverse_lazy('sentence_list')    
    

class UpdateSentence(AjaxableResponseMixin, UpdateView):
    model = Sentence
    fields = ['sentencename', 'subject' , 'verbid', 'receiver', 'resourceid', 'artefactid', 'datarealizado']
    success_url = reverse_lazy('sentence_list')

class DeleteSentence(DeleteView):
    model = Sentence
    success_url = reverse_lazy('sentence_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteSentence, self).delete(request, *args, **kwargs)
#==========   SENTENCE   ==========#    
    


    

#==========   GROUP   ==========#
class ListGroup(ListView):
    model = Group

class DetailGroup(DetailView):
    model = Group

class CreateGroup(AjaxableResponseMixin, CreateView):
    pkSentences = []
    model = Group
    fields = ['groupname']
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
        return super(CreateGroup, self).form_valid(form)
    success_url = reverse_lazy('group_list')

class UpdateGroup(AjaxableResponseMixin, UpdateView):
    model = Group
    fields = ['groupname', 'sentences']
    success_url = reverse_lazy('group_list')

class DeleteGroup(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request,f"a")
        return super(DeleteGroup, self).delete(request, *args, **kwargs)
#==========   GROUP   ==========#





#==========   PATTERN   ==========#
class ListPattern(ListView):
    model = Pattern

class DetailPattern(DetailView):
    model = Pattern

class CreatePattern(AjaxableResponseMixin, CreateView):
    model = Pattern
    fields = ['patternname', 'groups']
    def form_valid(self, form):
        form.instance.data_creation = timezone.now()
        form.instance.userid = self.request.user
        return super(CreatePattern, self).form_valid(form)
    success_url = reverse_lazy('pattern_list')

class UpdatePattern(AjaxableResponseMixin, UpdateView):
    model = Pattern
    fields = ['patternname', 'groups']
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

class DetailResource(DetailView):
    model = Resource

class CreateResource(AjaxableResponseMixin, CreateView):
    model = Resource
    fields = ['resourcename']
    success_url = reverse_lazy('resource_list')    
    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
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
#==========   RESOURCE   ==========#    
    




#==========   ARTEFACT   ==========#    
class ListArtefact(ListView):
    model = Artefact

class DetailArtefact(DetailView):
    model = Artefact

class CreateArtefact(AjaxableResponseMixin, CreateView):
    model = Artefact
    fields = ['artefactname']
    success_url = reverse_lazy('artefact_list')    
    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
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
#==========   ARTEFACT   ==========#