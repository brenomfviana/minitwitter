from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["get", "post"])
def ping(request):
    return Response({"message": "Success"}, status=status.HTTP_200_OK)
