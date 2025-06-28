from django.urls import path,include
from .views import MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', MessageViewSet, basename='mymessages')

urlpatterns = [
    path('', include(router.urls)),
]