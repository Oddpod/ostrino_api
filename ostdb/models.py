from django.db import models


class Show(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag


class OST(models.Model):
    title = models.CharField(max_length=100)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    video_id = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.title

