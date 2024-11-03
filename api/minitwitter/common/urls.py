from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HealthAPIView

router = DefaultRouter()

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health"),
]
