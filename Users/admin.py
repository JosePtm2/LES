from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profile, User, Organization

# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
