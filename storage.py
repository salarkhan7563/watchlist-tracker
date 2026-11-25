import json
import os

from models import Asset

FILE_PATH = "watchlist.json"


def save_watchlist(assets):
    data_to_save = [asset.to_dict() for asset in assets]
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data_to_save, file, indent=4)


def load_watchlist():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        loaded_assets = []
        for item in raw_data:
            asset = Asset.from_dict(item)
            loaded_assets.append(asset)
        return loaded_assets
