from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Process, Activity, Role, Product
from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib.auth.forms import UserCreationForm

# Register your models here.

admin.site.register(Process)
admin.site.register(Activity)
admin.site.register(Role)
admin.site.register(Product)

