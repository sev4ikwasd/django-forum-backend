from django.contrib import admin
from django.contrib.auth.models import Group

from profiles.admin import ProfileInline

from .models import User

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email',)
    inlines = (ProfileInline,)

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
