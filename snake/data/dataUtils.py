import json
from pathlib import Path

# config.json

def getConfig(config):
    mapFile = Path("snake/data/config.json")
    with open(mapFile) as f:
        d = json.load(f)
        return d[config]
