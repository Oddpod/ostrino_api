from django.shortcuts import render
from rest_framework import viewsets, serializers
from .models import OST, Show, Tag
from .serializers import OSTSerializer, ShowSerializer, TagSerializer


class OSTView(viewsets.ModelViewSet):
    queryset = OST.objects.all()
    serializer_class = OSTSerializer


class ShowView(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
