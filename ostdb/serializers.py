from rest_framework import serializers
from .models import OST, Show, Tag


class OSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OST
        fields = ('title', 'show', 'tags', 'video_id')


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
