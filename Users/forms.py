from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from tinymce.widgets import TinyMCE
from django.db import models
from .models import   User, Organization
from django.forms import ModelForm

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    organization = forms.ModelChoiceField(queryset=Organization.objects.all())
    class Meta:
        model = User
        fields = ("username", "email", "group", "organization", "password1", "password2",)
        

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        profile= self.cleaned_data.get('group')
        group = profile
        organization = self.cleaned_data['organization']
        if commit:
            user.save()
            user.groups.set(profile)
        return user
