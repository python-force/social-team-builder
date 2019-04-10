from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile')


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title