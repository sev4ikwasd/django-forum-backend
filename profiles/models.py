from django.db import models

class Profile(models.Model):

    user = models.OneToOneField('authentication.User', related_name='profile', on_delete=models.CASCADE)

    image = models.ImageField(upload_to='profile_images', blank=True)

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    