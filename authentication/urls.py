from . import  views
from django.urls import path

urlpatterns = [
    path('', views.Auth.as_view()),
]