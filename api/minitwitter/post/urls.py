from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FeedAPIView, PostViewSet

router = DefaultRouter()

router.register(
    r"posts",
    PostViewSet,
    basename="posts",
)

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedAPIView.as_view(), name="feed"),
]
