from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('OSTs', views.OSTView)
router.register('Shows', views.ShowView)
router.register('Tags', views.TagView)

urlpatterns = [
    path('', include(router.urls)),
    # todo move views to router
    url('^users/register/$', views.CreateUserAPIView.as_view(), name='register'),
    url('^users/login/$', views.UserLoginAPIView.as_view(), name='login')
]
