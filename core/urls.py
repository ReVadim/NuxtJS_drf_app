from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .core_api.api_views import PostViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
