import json
from pathlib import Path

# map.json

def getMap():
    mapFile = Path("snake/data/map.json")
    with open(mapFile) as f:
        d = json.load(f)
        return d["map"]

# config.json

def getConfig(config):
    mapFile = Path("snake/data/config.json")
    with open(mapFile) as f:
        d = json.load(f)
        return d[config]
