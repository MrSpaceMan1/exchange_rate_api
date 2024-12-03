from django.urls import path
from rest_framework import routers
from .views import get_rate, get_currencies

urlpatterns = [
    path("", get_currencies, name="get-currencies"),
    path("<currency_from_code>/<currency_to_code>", get_rate, name="get-rate")
]
