from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField

class Profile(models.Model):
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    description = MarkdownxField(blank=True)
    avatar = models.ImageField(blank=True)
    other_skills = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])


class Skill(models.Model):
    profile = models.ManyToManyField(Profile, related_name='skills', blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    timeline = models.CharField(max_length=255, blank=True)
    description = MarkdownxField(blank=True)
    applicant_requirements = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', args=[str(self.id)])


class Position(models.Model):
    project = models.ForeignKey(Project, related_name='positions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    description = MarkdownxField(blank=True)
    availability = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Position_Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    status = models.IntegerField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)