from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import FriendshipViewSet

router = DefaultRouter()
router.register(r'', FriendshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
]