from django.shortcuts import render
from rest_framework import viewsets
from .models import OST
from .serializers import OSTSerializer

# Create your views here.


class OSTView(viewsets.ModelViewSet):
    queryset = OST.objects.all()
    serializer_class = OSTSerializer