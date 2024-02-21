from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tracking.mixins import LoggingMixin


class MockNoLoggingView(APIView):

    def get(self, request):
        return Response("No Logging")


class MockLoggingView(LoggingMixin, APIView):
    def get(self, request):
        return Response("With Logging")


class MockExplicitLoggingView(LoggingMixin, APIView):
    logging_methods = ["POST"]

    def get(self, request):
        return Response("no Logging")

    def post(self, request):
        return Response("With Logging")


class MockCustomCheckLoggingView(LoggingMixin, APIView):
    def should_log(self, request, response):
        return "log" in response.data

    def get(self, request):
        return Response("with logging")

    def post(self, request):
        return Response("no record")


class MockSessionAuthLoggingView(LoggingMixin, APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("with logging")


class MockSensitiveFieldsLoggingView(LoggingMixin, APIView):
    sensitive_fields = {"mY_fIeLd"}

    def get(self, request):
        return Response("with logging")


class InvalidCleanSubstituteLoggingView(LoggingMixin, APIView):
    CLEAN_SUBSTITUTE = 1
