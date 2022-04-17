from rest_framework import serializers
from ..models import Post, Comment
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from django.contrib.auth.models import User
from taggit.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """ Tag serializer class """
    class Meta:
        model = Tag
        fields = ("name", "slug")
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """ Class PostSerializer """

    # tags = TagListSerializerField()
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'name', 'title', 'slug', 'description', 'content', 'image', 'created_at', 'author', 'tags']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ContactSerializer(serializers.Serializer):
    """ Serializer class for send email """
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """ Class for registration new users """
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password_confirm = validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Class User serializer """
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer class for comments """
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "username", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
