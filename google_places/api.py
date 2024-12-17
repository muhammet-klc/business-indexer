""" GOOGLE PLACE API """

import time
from typing import Dict, List, Tuple
import requests
from google_places.models import Place


class GooglePlacesAPI:
    """Class to interact with Google Places API."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def fetch_places_nearby(self, location: Tuple[float, float], radius: float, query: str) -> List[Dict]:
        """
        Fetch nearby places using Google Places Nearby Search API.
        """
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{location[0]},{location[1]}",
            "radius": radius,
            "keyword": query,  # For example, 'construction', 'real estate'
            "key": self.api_key,
        }
        places = []
        while True:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            places.extend(data.get("results", []))

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

            time.sleep(1)
            params["pagetoken"] = next_page_token

        return places

    def fetch_places_text(self, location: Tuple[float, float], radius: float, query: str) -> List[Dict]:
        """
        Fetch places using Google Places Text Search API.
        """
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "location": f"{location[0]},{location[1]}",
            "radius": radius,
            "query": query,  # For example, 'construction company', 'real estate agency'
            "key": self.api_key,
        }
        places = []
        while True:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            places.extend(data.get("results", []))

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

            time.sleep(1)
            params["pagetoken"] = next_page_token

        return places

    def fetch_place_details(self, place_id: str) -> Place:
        """
        Fetch detailed information for a specific place.
        """
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,website",
            "key": self.api_key,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        result = response.json().get("result", {})

        return Place(
            id=place_id,
            name=result.get("name"),
            address=result.get("formatted_address"),
            phone=result.get("formatted_phone_number"),
            website=result.get("website"),
        )
