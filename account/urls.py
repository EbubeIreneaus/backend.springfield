from . import views
from django.urls import path

urlpatterns = [
    path('details/<userId>', views.accountDetails),
]