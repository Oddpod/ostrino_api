from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from ostdb.custom_filters import OSTFilter, PlaylistFilter
from .models import OST, Show, Tag, Playlist
from .serializers import OSTSerializer, ShowSerializer, TagSerializer, CreateUserSerializer, \
    UserLoginSerializer, PlaylistSerializer, DetailPlaylistSerializer


class OSTView(viewsets.ModelViewSet):
    queryset = OST.objects.all().select_related('show')
    serializer_class = OSTSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OSTFilter

    def create(self, request, *args, **kwargs):
        show = request.data.get('show', "")
        Show.objects.update_or_create(name=show)
        tags = request.data.get('tags', [])
        for tag in tags:
            Tag.objects.get_or_create(tag=tag)
        return super(OSTView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            from django.db.models import Q
            return OST.objects.filter(Q(title__icontains=query) |
                                      Q(show__name__icontains=query) |
                                      Q(tags__tag__icontains=query)).distinct()
        elif not self.request.GET.get('ids', ''):
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
    filter_backends = (filters.DjangoFilterBackend,)


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class CreateUserAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = CreateUserSerializer


class PlaylistView(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PlaylistSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlaylistFilter

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super(PlaylistView, self).create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return PlaylistSerializer
        if self.action == 'retrieve':
            return DetailPlaylistSerializer
        return PlaylistSerializer

    def get_queryset(self):
        get_public = self.request.GET.get('public', '')
        if get_public:
            return Playlist.objects.all()
        # Return only users playlist by default
        return Playlist.objects.filter(created_by=self.request.user.id)


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
