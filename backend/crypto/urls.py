from django.urls import path
from . import views

urlpatterns = [
    path("coins/", views.coin_list, name="coin-list"),
    path("forecast/", views.forecast_list, name="forecast-list"),
    path("forecast/<str:symbol>/", views.forecast_detail, name="forecast-detail"),
    path("forecast/refresh/", views.refresh_forecasts, name="forecast-refresh"),
    path("forecast-refresh/", views.refresh_forecasts)
]
