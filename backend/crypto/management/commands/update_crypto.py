from django.core.management.base import BaseCommand
from crypto.services import fetch_and_update_prices

class Command(BaseCommand):
    help = "Fetch live crypto prices and update AI forecasts"

    def handle(self, *args, **kwargs):
        fetch_and_update_prices()
        self.stdout.write(self.style.SUCCESS("Crypto prices & forecasts updated!"))
