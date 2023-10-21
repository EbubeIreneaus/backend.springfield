from . import views
from django.urls import path

urlpatterns = [
    path('details/<int:userId>', views.accountDetails),
]