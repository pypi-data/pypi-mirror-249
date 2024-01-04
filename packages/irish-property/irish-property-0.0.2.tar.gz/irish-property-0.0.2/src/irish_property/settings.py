import os
import json
from pathlib import Path
from enum import Enum
from typing import List

from daft_scraper.search.options import PropertyType
from daft_scraper.search.options_location import Location

from irish_property.constants import MYHOME_REGIONS, MYHOME_PROPERTY_TYPES

LOG_LOCATION = (
    "/var/log/irish_property/irish_property.log"
    if os.getenv("TEST_ENV", "False") == "False"
    else "/tmp/log/irish_property/irish_property.log"
)
DATA_LOCATION = os.getenv("DATA_LOCATION", "/opt/irish_property")
SHELVE_LOCATION = os.getenv(
    "SHELVE_LOCATION", os.path.join(DATA_LOCATION, "shelved_data")
)
CONFIGS_LOCATION = os.getenv("CONFIGS_LOCATION", os.path.join(DATA_LOCATION, "configs"))

os.makedirs(CONFIGS_LOCATION, exist_ok=True)


def get_json(fp):
    data = None
    try:
        with open(fp, "r") as fh:
            data = json.loads(fh.read())
    except Exception:
        from irish_property import logger

        logger.error(f"Failed to load config: {fp}")
        return None

    return data


def get_configs() -> List[Enum]:
    config_filenames = os.listdir(CONFIGS_LOCATION)
    if len(config_filenames) == 0:
        from irish_property import logger

        logger.warning("No configs found")
        return []

    configs = []
    for config_filename in config_filenames:
        if not Path(config_filename).suffix == ".json":
            continue

        fp = os.path.join(CONFIGS_LOCATION, config_filename)

        data = get_json(fp)
        if data["DAFT_LOCATIONS"]:
            data["DAFT_LOCATIONS"] = [
                getattr(Location, l) for l in data["DAFT_LOCATIONS"]
            ]

        if data["DAFT_PROPERTY_TYPES"]:
            data["DAFT_PROPERTY_TYPES"] = [
                getattr(PropertyType, p) for p in data["DAFT_PROPERTY_TYPES"]
            ]

        if data["MYHOME_REGION"]:
            data["MYHOME_REGION"] = getattr(MYHOME_REGIONS, data["MYHOME_REGION"]).value

        if data["MYHOME_PROPERTY_TYPES"]:
            data["MYHOME_PROPERTY_TYPES"] = [
                getattr(MYHOME_PROPERTY_TYPES, p).value
                for p in data["MYHOME_PROPERTY_TYPES"]
            ]

        configs.append(Enum("Config", list(data.items())))

    return configs
