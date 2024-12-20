""" PLACE APP """

import os
import json
import time
from typing import List, Optional
from google_places.api import GooglePlacesAPI
from google_places.manager import PlaceSearchManager
from google_places.models import Grid
# from utils.file import save_to_file


class PlaceApp:
    def __init__(self, api_key: str, queries: Optional[List[str]], output_dir: Optional[str]):

        self.API_KEY = api_key
        self.QUERIES = queries
        self.OUTPUT_DIR = output_dir

        # Konfigürasyonlar
        km_to_degree = 1 / 111  # 1 km'yi dereceye dönüştürme faktörü
        self.distance_km = 5  # Her karenin kenar uzunluğu 5 km
        self.STEP_SIZE = self.distance_km * km_to_degree  # 5 km'yi dereceye dönüştür
        self.RADIUS = 1000 * self.distance_km / 2  # km yarıçap

        # Grid koordinatları
        self.TOP_LEFT = (41.30, 28.1)
        self.BOTTOM_RIGHT = (40.9, 29.1)

        # API ve manager başlat
        self.google_places_api = GooglePlacesAPI(api_key=self.API_KEY)
        self.search_manager = PlaceSearchManager(api=self.google_places_api)

        # Grid oluştur
        self.grid_coordinates = Grid.create_grid(self.TOP_LEFT, self.BOTTOM_RIGHT, self.STEP_SIZE)

        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

    def read_existing_ids(self, filename: str) -> set:
        """Read existing IDs from the file and return as a set."""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:  # Use utf-8 encoding
                data = json.load(file)
                return {place['id'] for place in data.get('results', [])}
        return set()

    def write_new_places(self, filename: str, places: list):
        """Write new places to the file."""
        existing_ids = self.read_existing_ids(filename)
        
        # Filter out places with existing IDs
        new_places = [place for place in places if place.id not in existing_ids]  # Use 'place.id'
        if new_places:
            # Load existing data if file exists
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:  # Use utf-8 encoding
                    data = json.load(file)
                    data['results'].extend([place.to_dict() for place in new_places])  # Convert Place objects to dict
            else:
                # If the file doesn't exist, create new data
                data = {'results': [place.to_dict() for place in new_places]}  # Create initial data
            
            with open(filename, 'w', encoding='utf-8') as file:  # Use utf-8 encoding
                json.dump(data, file, indent=4, ensure_ascii=False)  # Prevent ASCII escape sequences
            print(f"Added {len(new_places)} new places to '{filename}'")
        else:
            print(f"No new places found for '{filename}'")

    def process_queries(self):
        total_coords_length = len(self.grid_coordinates)

        for index, coord in enumerate(self.grid_coordinates[167:], 167):
            print(f"Processing coordinate {index + 1}/{total_coords_length}, coordinate: {coord}")

            for query in self.QUERIES:
                print(f"Processing query: {query}")
                places = self.search_manager.get_places_and_details(coord, self.RADIUS, query)
                filename = os.path.join(self.OUTPUT_DIR, "business_results.json")
                self.write_new_places(filename, places)

                print(f"Results for '{query}' saved to {filename}")
                time.sleep(1)

    def run(self):
        # Sorguları işleme
        self.process_queries()
