from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Verb, Sentence, Group, Pattern
from django.template.loader import render_to_string
from django.utils import timezone

# Create your views here.


class ListVerb(ListView):
    model = Verb


class DetailVerb(DetailView):
    model = Verb


class CreateVerb(CreateView):
    model = Verb
    fields = ['verbname', 'verbtype']
    success_url = reverse_lazy('verb_list')


class UpdateVerb(UpdateView):
    model = Verb
    fields = ['verbname', 'verbtype']
    success_url = reverse_lazy('verb_list')


class DeleteVerb(DeleteView):
    model = Verb
    success_url = reverse_lazy('verb_list')


class ListSentence(ListView):
    model = Sentence
    

class DetailSentence(DetailView):
    model = Sentence

    
class CreateSentence(CreateView):
    model = Sentence
    fields = ['sentencename', 'subject', 'receiver', 'verbid', 'artefacto']

    def form_valid(self, form):
        form.instance.datecreated = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateSentence, self).form_valid(form)

    success_url = reverse_lazy('sentence_list')
    

class UpdateSentence(UpdateView):
    model = Sentence
    fields = ['sentencename', 'subject', 'verbid', 'userid']
    success_url = reverse_lazy('sentence_list')


class DeleteSentence(DeleteView):
    model = Sentence
    success_url = reverse_lazy('sentence_list')


class ListGroup(ListView):
    model = Group


class DetailGroup(DetailView):
    model = Group


class CreateGroup(CreateView):
    model = Group
    fields = ['groupname']

    def form_valid(self, form):
        form.instance.creationdate = timezone.now()
        form.instance.userid = self.request.user
        return super(CreateGroup, self).form_valid(form)

    success_url = reverse_lazy('group_list')


class UpdateGroup(UpdateView):
    model = Group
    fields = ['userid', 'groupname']
    success_url = reverse_lazy('group_list')


class DeleteGroup(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')


class ListPattern(ListView):
    model = Pattern


class DetailPattern(DetailView):
    model = Pattern


class CreatePattern(CreateView):
    model = Pattern
    fields = ['patternname']

    def form_valid(self, form):
        form.instance.data_creation = timezone.now()
        form.instance.userid = self.request.user
        return super(CreatePattern, self).form_valid(form)

    success_url = reverse_lazy('pattern_list')


class UpdatePattern(UpdateView):
    model = Pattern
    fields = ['userid', 'patternname']
    success_url = reverse_lazy('pattern_list')


class DeletePattern(DeleteView):
    model = Pattern
    success_url = reverse_lazy('pattern_list')
