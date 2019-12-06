import json
from pathlib import Path

# config.json

def getConfig(config):
    mapFile = Path("C:/Users/Fred/Desktop/CSI4506/Projet/CSI4506-project/snake/data/config.json")
    with open(mapFile) as f:
        d = json.load(f)
        return d[config]
