from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('OSTs', views.OSTView)
router.register('Shows', views.ShowView)
router.register('Tags', views.TagView)

urlpatterns = [
    path('', include(router.urls))

]
