from rest_framework import viewsets
from .serializers import PostSerializer
from ..models import Post
from rest_framework.response import Response


class PostViewSet(viewsets.ViewSet):
    """ Class Post ViewSet """

    parser_classes = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'