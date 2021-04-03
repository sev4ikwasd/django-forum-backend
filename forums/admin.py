from django.contrib import admin

from .models import *

class ForumAdmin(admin.ModelAdmin):
    search_fields = ('title', 'slug')

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
    date_hierarchy = 'created_time'
    search_fields = ('title',)
    autocomplete_fields = ('forum', 'creator')

    #This is required to not show slug on creation
    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or []

        if not obj:
            return excluded + ['slug']

        return excluded
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj) or []

        if obj:
            return readonly + ['slug', 'created_time', 'changed_time']

        return readonly

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'written_time'
    fields = ('text', 'topic', 'author', 'written_time', 'changed_time')
    readonly_fields = ('written_time', 'changed_time')
    autocomplete_fields = ('topic', 'author',)

admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
