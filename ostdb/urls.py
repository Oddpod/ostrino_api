from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views

router = routers.DefaultRouter()
router.register('OSTs', views.OSTView)
router.register('Shows', views.ShowView)
router.register('Tags', views.TagView)
router.register('Playlists', views.PlaylistView)


urlpatterns = [
    path('', include(router.urls)),
    # todo move views to router
    url('^users/register', views.CreateUserAPIView.as_view(), name='register'),
    url('^users/login', views.UserLoginAPIView.as_view(), name='login'),
    url('^auth/obtain_token', obtain_jwt_token),
    url('^auth/refresh_token', refresh_jwt_token),
]
