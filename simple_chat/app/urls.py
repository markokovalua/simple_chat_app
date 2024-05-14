from .views import ThreadViewSet, MessageViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'threads', ThreadViewSet, basename='thread')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path("api/", include(router.urls))
]