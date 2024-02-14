from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/<str:username>/', views.About.as_view(), name='about'),
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('writers/', views.WritersView.as_view(), name='writers'),
]
