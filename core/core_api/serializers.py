from rest_framework import serializers
from ..models import Post
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from django.contrib.auth.models import User


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """ Class PostSerializer """

    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'name', 'title', 'slug', 'description', 'content', 'image', 'created_at', 'author', 'tags']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
