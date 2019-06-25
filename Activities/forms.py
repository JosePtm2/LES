from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Sentence


class SentenceForm(forms.ModelForm):


    def clean(self):
        super(SentenceForm, self).clean()
        if bool(self.cleaned_data['verbid']) == bool(
                self.cleaned_data['verb_sug']):
            raise ValidationError("Please, fill the first or second field")

    class Meta:
        model = Sentence
        fields = ['sentencename', 'subject', 'verb_sug', 'verbid',
                  'receiver', 'resourceid', 'artefactid', 'datarealizado']
