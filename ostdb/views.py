from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import OST, Show, Tag, Playlist
from .serializers import OSTSerializer, ShowSerializer, TagSerializer, CreateUserSerializer, \
    UserLoginSerializer, PlaylistSerializer


class OSTView(viewsets.ModelViewSet):
    queryset = OST.objects.all().select_related('show').prefetch_related('tags')
    serializer_class = OSTSerializer

    def create(self, request, *args, **kwargs):
        show = request.data['show']
        Show.objects.update_or_create(name=show)
        tags = request.data['tags']
        for tag in tags:
            Tag.objects.get_or_create(tag=tag)
        return super(OSTView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.GET.get('ids', ''):
            return OST.objects.all()
        string_ids = self.request.GET.get('ids', '').replace('[', '').replace(']','')
        ids = [int(s) for s in string_ids.split(',')]
        if ids:
            osts = OST.objects.filter(pk__in=ids)
        else:
            osts = OST.objects.all()
        return osts




class ShowView(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ShowSerializer


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreateUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    #queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class PlaylistView(viewsets.ModelViewSet):
    queryset = Playlist.objects.filter(public=True)
    permission_classes = [AllowAny]
    serializer_class = PlaylistSerializer


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
