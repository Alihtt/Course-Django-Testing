from rest_framework.response import Response
from rest_framework.views import APIView
from tracking.mixins import LoggingMixin


class MockNoLoggingView(APIView):

    def get(self, request):
        return Response("No Logging")


class MockLoggingView(LoggingMixin, APIView):
    def get(self, request):
        return Response("With Logging")
