from django.contrib import admin
from stb.core.models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

"""
Appends Profile to User in Django Admin

class MyCustomUserInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name = Profile

class MyUserAdmin(BaseUserAdmin):
    inlines = (MyCustomUserInline, )

admin.site.unregister(MyCustomUser)
admin.site.register(MyCustomUser, MyUserAdmin)
"""
