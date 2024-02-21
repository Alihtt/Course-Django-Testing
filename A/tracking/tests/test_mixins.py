import ast
import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APIRequestFactory, APITestCase

from tracking.base_mixins import BaseLoggingMixin
from tracking.models import ApiRequestLog

from .views import MockLoggingView


@override_settings(ROOT_URLCONF="tracking.tests.urls")
class TestLoggingMixin(APITestCase):
    def test_no_logging_no_log_created(self):
        self.client.get("/no-logging/")
        self.assertEqual(ApiRequestLog.objects.all().count(), 0)

    def test_logging_created(self):
        self.client.get("/logging/")
        self.assertEqual(ApiRequestLog.objects.all().count(), 1)

    def test_log_path(self):
        self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.path, "/logging/")

    def test_log_ip_remote(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "127.0.0.9"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.9")

    def test_log_ip_remote_list(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "127.0.0.9, 128.0.0.1"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.9")

    def test_log_ip_remote_v4_with_port(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "127.0.0.9:8888"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.9")

    def test_log_ip_remote_v6(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "2001:db8:85a3::8a2e:370:7334")

    def test_log_ip_remote_v6_loopback(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "::1"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "::1")

    def test_log_ip_remote_v6_with_port(self):
        request = APIRequestFactory().get("logging")
        request.META["REMOTE_ADDR"] = "[::1]:1234"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "::1")

    def test_log_ip_xforwarded(self):
        request = APIRequestFactory().get("logging")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.8"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.8")

    def test_log_ip_xforwarded_list(self):
        request = APIRequestFactory().get("logging")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.8, 128.0.0.9"
        MockLoggingView.as_view()(request).render()
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.remote_addr, "127.0.0.8")

    def test_log_host(self):
        self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.host, "testserver")

    def test_log_method(self):
        self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.method, "GET")

    def test_log_status_code(self):
        self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.status_code, 200)

    def test_log_explicit(self):
        self.client.get("/explicit-logging/")
        self.client.post("/explicit-logging/")
        self.assertEqual(ApiRequestLog.objects.all().count(), 1)

    def test_log_custom_check(self):
        self.client.get("/custom-check-logging/")
        self.client.post("/custom-check-logging/")
        self.assertEqual(ApiRequestLog.objects.all().count(), 1)

    def test_log_anon_user(self):
        self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.user, None)

    def test_log_session_auth_user(self):
        user = User.objects.create_user(username="myname", password="mypass")
        self.client.login(username="myname", password="mypass")
        self.client.get("/session-auth-logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(log.user, user)

    def test_log_params(self):
        self.client.get("/logging/", {"a": "1234"})
        log = ApiRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params), {"a": "1234"})

    def test_log_sensitive_fields_params(self):
        self.client.get(
            "/sensitive-fields-logging/",
            {"api": "1234", "detail": "Test", "my_field": "5678"},
        )
        log = ApiRequestLog.objects.first()
        self.assertEqual(
            ast.literal_eval(log.query_params),
            {
                "api": BaseLoggingMixin.CLEAN_SUBSTITUTE,
                "detail": "Test",
                "my_field": BaseLoggingMixin.CLEAN_SUBSTITUTE,
            },
        )

    def test_log_invalid_clean_substitute(self):
        with self.assertRaises(AssertionError):
            self.client.get("/invalid-clean-substitute-logging/")

    @mock.patch("tracking.models.ApiRequestLog.save")
    def test_log_doesnt_fail_if_model_save_failed(self, mock_save):
        mock_save.side_effect = Exception("db failure")
        response = self.client.get("/logging/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApiRequestLog.objects.all().count(), 0)

    @override_settings(USE_TZ=False)
    @mock.patch("tracking.base_mixins.now")
    def test_log_doesnt_fail_with_negative_response_ms(self, mock_now):
        mock_now.side_effect = [
            datetime.datetime(2019, 1, 1, 10, 0, 10),
            datetime.datetime(2019, 1, 1, 10, 0, 0),
        ]
        response = self.client.get("/logging/")
        log = ApiRequestLog.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(log.response_ms, 0)
