"""Get and set lattitude and long for specific location."""
import os
from typing import List

import geocoder

from twitter.twitter_authenticator import create_api

api = create_api()


LOCATION = os.getenv("LOCATION", "Mexico")


def set_lat_long_for_location() -> tuple:
    """Set lat and long for specific location.

    :return tupe: lat and long
    """
    geolocation = geocoder.osm(location=LOCATION)
    return geolocation.lat, geolocation.lng


def get_trending_by_location() -> List:
    """Get trending topics by given location.

    :return List: trending topic list.
    """
    closest_loc = api.trends_closest(*set_lat_long_for_location())
    return api.trends_place(closest_loc[0]["woeid"])
