from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import LoggingMixin


class Home(LoggingMixin, APIView):
    sensitive_fields = {"pass"}

    def post(self, request):
        return Response("Hello")
