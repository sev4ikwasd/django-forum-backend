from django.contrib import admin

from .models import *

class ForumAdmin(admin.ModelAdmin):
    #This is required to not show slug on creation
    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []

        if not obj:
            return excluded + ['slug']

        return excluded
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj) or []

        if obj:
            return readonly + ['slug']

        return readonly

class TopicAdmin(admin.ModelAdmin):
    #This is required to not show slug on creation
    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []

        if not obj:
            return excluded + ['slug']

        return excluded
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj) or []

        if obj:
            return readonly + ['slug']

        return readonly

admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
