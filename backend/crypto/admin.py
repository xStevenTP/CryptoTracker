from django.contrib import admin
from .models import Coin, Forecast

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "price", "last_updated")
    search_fields = ("symbol", "name")

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ("coin", "created_at", "suggestion")
    list_filter = ("coin", "created_at")
