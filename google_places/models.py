""" GOOGLE PLACE MODELS """

from typing import Dict, List, Tuple, Optional


class Place:
    """Model class representing a place and its details."""

    def __init__(
        self,
        id: Optional[str],
        name: Optional[str],
        address: Optional[str],
        phone: Optional[str],
        website: Optional[str],
    ) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website

    def to_dict(self) -> Dict:
        """
        Convert the Place instance to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "website": self.website
        }


class Grid:
    """Model class to handle the creation of grid coordinates."""

    @staticmethod
    def create_grid(nw: Tuple[float, float], se: Tuple[float, float], step: float) -> List[Tuple[float, float]]:
        """
        Create a grid of coordinates within the specified bounds.
        """
        lat, lon = nw
        coordinates = []

        while lat > se[0]:
            lon = nw[1]
            while lon < se[1]:
                center_lat = lat - (step / 2)
                center_lon = lon + (step / 2)
                coordinates.append((center_lat, center_lon))
                lon += step
            lat -= step

        return coordinates
