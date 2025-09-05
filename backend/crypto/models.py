from django.db import models

class Coin(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Forecast(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="forecasts")
    forecast_data = models.JSONField()
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forecast for {self.coin.symbol} at {self.created_at}"
