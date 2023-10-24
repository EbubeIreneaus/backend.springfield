from . import  views
from django.urls import path

urlpatterns = [
    path('', views.Auth.as_view()),
    path('resend_link/', views.resend_link),
    path('verify/', views.verify_account),
]