import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Coin, Forecast
from .serializers import CoinSerializer, ForecastSerializer
from django.utils import timezone

COINGECKO_API = "https://api.coingecko.com/api/v3"
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001/predict")

@api_view(["POST"])
def refresh_forecasts(request):
    print(">>> refresh_forecasts CALLED")
    
    """
    Refresh forecasts for all coins:
    - Fetch recent prices from CoinGecko
    - Call AI microservice for prediction
    - Save forecast in DB
    """
    
    results = []
    for coin in Coin.objects.all():
        try:
            # 1️⃣ Fetch historical prices (last 10 days daily close price)
            cg_url = f"{COINGECKO_API}/coins/{coin.symbol.lower()}/market_chart"
            params = {"vs_currency": "usd", "days": "10", "interval": "daily"}
            resp = requests.get(cg_url, params=params)
            data = resp.json()

            if "prices" not in data:
                continue

            # Extract just the price values
            prices = [p[1] for p in data["prices"]]

            # 2️⃣ Call AI microservice
            ai_resp = requests.post(AI_SERVICE_URL, json={"coin": coin.symbol, "prices": prices})
            ai_data = ai_resp.json()

            forecast_data = ai_data.get("forecast", [])
            suggestion = ai_data.get("suggestion", "")

            # 3️⃣ Save forecast to DB
            forecast = Forecast.objects.create(
                coin=coin,
                forecast_data=forecast_data,
                suggestion=suggestion,
                created_at=timezone.now(),
            )

            results.append(ForecastSerializer(forecast).data)

        except Exception as e:
            print(f"Error refreshing {coin.symbol}: {e}")
            continue

    return Response({"status": "ok", "updated": len(results), "forecasts": results})

@api_view(["GET"])
def coin_list(request):
    coins = Coin.objects.all()
    serializer = CoinSerializer(coins, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def forecast_list(request):
    """
    Return the most recent forecast for each coin.
    """
    forecasts = []
    for coin in Coin.objects.all():
        latest_forecast = Forecast.objects.filter(coin=coin).order_by("-created_at").first()
        if latest_forecast:
            forecasts.append(latest_forecast)

    serializer = ForecastSerializer(forecasts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def forecast_detail(request, symbol):
    """
    Return only the most recent forecast for a given coin.
    """
    coin = get_object_or_404(Coin, symbol=symbol.upper())
    forecast = Forecast.objects.filter(coin=coin).order_by("-created_at").first()

    if not forecast:
        return Response({"error": "No forecast available"}, status=404)

    serializer = ForecastSerializer(forecast)
    return Response(serializer.data)
