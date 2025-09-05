from rest_framework import serializers
from .models import Coin, Forecast

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ["symbol", "name", "price", "last_updated"]

class ForecastSerializer(serializers.ModelSerializer):
    coin = serializers.CharField(source="coin.name", read_only=True)

    class Meta:
        model = Forecast
        fields = ["forecast_data", "suggestion", "created_at", "coin"]
