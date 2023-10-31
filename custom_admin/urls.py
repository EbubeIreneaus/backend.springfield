from . import views
from django.urls import path

urlpatterns = [
    path('getTransaction/', views.getTransaction),
    path('approve/', views.approveTransaction),
    path('reject/', views.rejectTransaction),
    path('auth', views.auth),
]