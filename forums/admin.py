from django.contrib import admin

from .models import *

class ForumAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class TopicAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
