from django.urls import path,include
from .views import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]