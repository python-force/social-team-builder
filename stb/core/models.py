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
    profile = models.ForeignKey(Profile, related_name='skills', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    timeline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    applicant_requirements = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', args=[str(self.id)])


class Position(models.Model):
    project = models.ForeignKey(Project, related_name='positions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title