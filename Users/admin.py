#from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profile, User, Organization, Permission
from django.contrib.auth.models import Group

# Register your models here.

class UserAdmin(admin.ModelAdmin):
	fieldsets = (
        (None, {'fields': ('username', 'useremail', 'password','organizationid')}),
        (('Permissions'), {'fields': ('groups',)}),
    )

class PermissionAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Permission, PermissionAdmin)
