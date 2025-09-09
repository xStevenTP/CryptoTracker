import requests
from django.utils import timezone
from .models import Coin, Forecast

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001/predict")

def fetch_and_update_prices(symbols=["bitcoin", "ethereum", "dogecoin"]):
    """
    Fetch live crypto prices from CoinGecko and update DB.
    After updating, call AI microservice for forecast/suggestions.
    """
    ids = ",".join(symbols)
    try:
        response = requests.get(f"{COINGECKO_URL}?ids={ids}&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching CoinGecko data: {e}")
        return

    for sym in symbols:
        coin_name = sym.capitalize()
        price = data[sym]["usd"]

        coin, _ = Coin.objects.update_or_create(
            symbol=sym.upper(),
            defaults={"name": coin_name, "price": price, "last_updated": timezone.now()},
        )

        # Call AI service for suggestion
        call_ai_forecast(coin)


def call_ai_forecast(coin: Coin):
    """
    Send recent prices to AI service and store forecast + suggestion.
    """
    prices = [float(coin.price)] * 10  # Replace with real historical data if available
    payload = {"coin": coin.symbol, "prices": prices}

    try:
        res = requests.post(AI_SERVICE_URL, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()

        Forecast.objects.create(
            coin=coin,
            forecast_data=data.get("forecast", []),
            suggestion=data.get("suggestion", "No suggestion"),
        )

    except Exception as e:
        print(f"AI service error for {coin.symbol}: {e}")
