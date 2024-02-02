__author__ = 'Taras Dubrava'
__date__ = 'January 2024'
__copyright__ = '(C) 2024, Taras Dubrava'

# imports
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from datetime import datetime


def truncator(coord: float, prec: int) -> float:
    return float(str(coord)[:str(coord).find('.') + prec + 1])


async def get_location(input_loc: str) -> dict:
    async with Nominatim(user_agent="visitedplaces", timeout=10, adapter_factory=AioHTTPAdapter) as geolocator:
        result = {}
        try:
            location = await geolocator.geocode(input_loc, language="en", exactly_one=True, addressdetails=True)
            if not (location is None):
                result = {
                    "id": 1,
                    "place": location.raw['address'].get(location.raw['addresstype']),
                    "country": location.raw['address']['country'],
                    "lat": truncator(location.latitude, 6),
                    "lon": truncator(location.longitude, 6),
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
        except Exception as e:
            print('Exception in get_location', e)

        return result
