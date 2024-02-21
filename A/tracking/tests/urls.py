from django.urls import path

from . import views

urlpatterns = [
    path("no-logging/", views.MockNoLoggingView.as_view()),
    path("logging/", views.MockLoggingView.as_view()),
]
