from rest_framework import serializers
from .models import OST


class OSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OST
        fields = ('title', 'show', 'tags', 'video_id')