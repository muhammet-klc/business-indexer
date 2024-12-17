""" GOOGLE PLACE MANAGER """

import time
from typing import List, Tuple
from .api import GooglePlacesAPI
from .models import Place


class PlaceSearchManager:
    """Manager class to handle grid search and fetching place details."""

    def __init__(self, api: GooglePlacesAPI) -> None:
        self.api = api

    def get_places_and_details(
        self, coord: Tuple[float, float], radius: float, query: str
    ) -> List[Place]:
        """
        Fetch places and their details for all grid coordinates.
        """
        all_places = []

        places = self.api.fetch_places_text(coord, radius, query)
        print(f"Found {len(places)} places.")

        for place in places:
            place_id = place["place_id"]
            details = self.api.fetch_place_details(place_id)
            all_places.append(details)

            print(f"Place ID: {place_id} indexed")
            
            time.sleep(1)
        return all_places
