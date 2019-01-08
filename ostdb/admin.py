from django.contrib import admin
from .models import OST, Show, Tag, Playlist

# Register your models here.

admin.site.register(OST)
admin.site.register(Show)
admin.site.register(Tag)
admin.site.register(Playlist)
