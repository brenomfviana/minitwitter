from datetime import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class HealthAPIView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request) -> Response:
        data = {
            "status": "It's fine!",
            "datetime": datetime.now(),
        }
        return Response(data=data, status=status.HTTP_200_OK)
