import django
from django.db import models
from django.core import validators
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group
from Users.models import User
from Activities.models import Pattern
from django.core.exceptions import ValidationError

# Create your models here.

class Process(models.Model):
    process_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField("date created", default=django.utils.timezone.now)
    description = models.TextField(max_length=200)



    def __str__(self):
        return self.process_name

class Activity(models.Model):
    activity_name = models.CharField(max_length=200)
    process = models.ForeignKey(Process, null=True,blank=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=200)
    role = models.ManyToManyField('Role', blank=True)
    original = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL)
    pattern = models.ManyToManyField('Activities.Pattern', blank=True)
    class Meta:
        verbose_name = ("Activity") 

    def __str__(self):
        return self.activity_name

    def clean(self):
        incident = Activity.objects.filter(activity_name=self.activity_name).exclude(process__isnull=False)
        if incident and self.original is None:
                if not Activity.objects.filter(id=self.pk).exists() : # check if any object exists
                    raise ValidationError('Já existe uma Actividade Base com este nome.')
                elif not incident[0].pk == self.pk: 
                    raise ValidationError('Já existe uma Actividade Base com este nome.')
class Role(models.Model):
    role_name = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    def __str__(self):
        return self.role_name



class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=1)
    product_format = models.CharField(max_length=200)
    activity = models.ManyToManyField(Activity, blank=True)

    def __str__(self):
        return self.product_name
