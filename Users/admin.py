from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Profile, User, Organization, Permission

# Register your models here.


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
