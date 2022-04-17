from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import filters
from api.settings import EMAIL_HOST_USER
from .serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, \
    CommentSerializer
from ..models import Post, Comment
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import generics
from taggit.models import Tag


class PageNumberSetPagination(pagination.PageNumberPagination):
    """ Simple pagination for class Post """
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostViewSet(viewsets.ModelViewSet):
    """ Class Post ViewSet """
    search_fields = ['content', 'name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    """ View for tags in Post model """
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    """ View for tags in models """
    serializer_class = TagSerializer()
    queryset = Tag.objects.all()
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    """ Aside part of page """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    """ View for feedback and send email """
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'From {name} | {subject}', f'From: {from_email}\n\n{message}', from_email, [EMAIL_HOST_USER])
            return Response({'success': "Sent"})


class RegisterView(generics.GenericAPIView):
    """ View class for new user registration """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан'
        })


class ProfileView(generics.GenericAPIView):
    """ A class for displaying user information """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"user": UserSerializer(request.user, context=self.get_serializer_context()).data, })


class CommentView(generics.ListCreateAPIView):
    """ Class for view comments """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)
