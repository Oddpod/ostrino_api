from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from .models import OST, Show, Tag, Playlist


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return super(TagSerializer, self).create(validated_data)

    def validate(self, attrs):
        slugTag = slugify(attrs.get('tag'))
        return super(TagSerializer, self).validate(attrs)


class OSTSerializer(serializers.ModelSerializer):
    show = serializers.SlugRelatedField(queryset=Show.objects.all(), slug_field='name')

    class Meta:
        model = OST
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        name = validated_data['name']
        if not user:
            user = validated_data['created_by']
        osts = validated_data['osts']
        public = validated_data['public']
        new_playlist = Playlist(name=name, created_by=user, public=public)
        new_playlist.save()
        if osts:
            new_playlist.osts.set(osts)
        return validated_data


# Override osts on detail view to get whole ost
class DetailPlaylistSerializer(PlaylistSerializer):
    osts = OSTSerializer(many=True, read_only=True)


class CreateUserSerializer(ModelSerializer):
    email1 = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm email')

    class Meta:
        model = User
        fields = [
            'username',
            'email1',
            'email2',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email1')
        email2 = value
        if email1 != email2:
            raise ValidationError('The emails must match')
        user_query = User.objects.filter(email=email2)
        if user_query.exists():
            raise ValidationError("A user with this email already exists")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email2']
        password = validated_data['password']
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, attrs):
        user_obj = None
        email = attrs.get("email", None)
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        if not email and not username:
            raise ValidationError("Please enter a username or email.")

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
            ).distinct()
        user = user.exclude(email__isnull=True)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid." + str(user))

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password, please try again")

        attrs["token"] = "SOME RANDOM TOKEN"
        return attrs
