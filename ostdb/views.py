from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import OST, Show, Tag, Playlist
from .serializers import OSTSerializer, ShowSerializer, TagSerializer, CreateUserSerializer, UserLoginSerializer, \
    PlaylistSerializer


class OSTView(viewsets.ModelViewSet):
    queryset = OST.objects.all()
    serializer_class = OSTSerializer


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


class CreatePlaylist(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def retrieve(self, request, pk=None, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        playlists = Playlist.objects.filter(created_by=user)
        return Response(playlists)


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
