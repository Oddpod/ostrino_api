from django.contrib.auth.models import User
from django.db import models


class Show(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.SlugField(max_length=20, primary_key=True)

    def __str__(self):
        return self.tag


class OST(models.Model):
    title = models.CharField(max_length=100)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    video_id = models.CharField(max_length=12, null=True, unique=True)
    spotify_id = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    osts = models.ManyToManyField(OST, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ', by: ' + str(self.created_by)

    class Meta:
        unique_together = ('created_by', 'name')
