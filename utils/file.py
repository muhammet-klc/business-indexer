""" FILE """

import json


def save_to_file(data, filename):
    """Save JSON data to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
