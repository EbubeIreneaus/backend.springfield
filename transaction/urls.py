from . import views
from django.urls import path

urlpatterns = [
	path('', views.Transactions.as_view()),
]