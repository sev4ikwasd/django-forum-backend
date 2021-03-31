from django.db import models

from core.utils import unique_slugify

from authentication.models import User

def get_deleted_user():
    return User.objects.get_or_create(username='deleted', email='', password='', is_active=False)[0]

class Forum(models.Model):
    title = models.CharField(db_index=True, max_length=255)
    slug = models.SlugField(db_index=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title) 
        super(Forum, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class Topic(models.Model):
    title = models.CharField(db_index=True, max_length=255)
    slug = models.SlugField(db_index=True, unique=True, blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='topics')
    creator = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name='started_topics')
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title) 
        super(Topic, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name='comments')
    written_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        result = self.text
        if len(result) > 30:
            result = result[:30] + '...'
        return result
