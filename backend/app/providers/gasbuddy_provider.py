# Заглушка для получения цен на дизель
from app.core.interfaces.fuel_provider import FuelProvider

class GasBuddyProvider(FuelProvider):
    def get_prices(self, lat, lon):
        return [{"station": "Pilot", "price": 3.79}, {"station": "Loves", "price": 3.84}]

