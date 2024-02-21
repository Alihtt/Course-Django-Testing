from django.urls import path

from . import views

urlpatterns = [
    path("no-logging/", views.MockNoLoggingView.as_view()),
    path("logging/", views.MockLoggingView.as_view()),
    path("explicit-logging/", views.MockExplicitLoggingView.as_view()),
    path("custom-check-logging/", views.MockCustomCheckLoggingView.as_view()),
    path("session-auth-logging/", views.MockSessionAuthLoggingView.as_view()),
    path("sensitive-fields-logging/", views.MockSensitiveFieldsLoggingView.as_view()),
    path(
        "invalid-clean-substitute-logging/",
        views.InvalidCleanSubstituteLoggingView.as_view(),
    ),
]
