import os
from PIL import Image
import json
from enum import Enum
import numpy as np
import random

"""
    draw from pool of 10000 attributes from each trait
    function to generate metadata for all 10000 images
"""

TOTAL_ITEMS = 10000

class Trait(Enum):
    BACKGROUND = 0
    FUR = 1
    EYES = 2
    CLOTHES = 3
    ACCESSORIES = 4
    FACE = 5
    HAT = 6

TRAIT_SUPPLY = {
    "background": {
        "total": 9995
    },
    "clothes": {
        "total": 9995
    },
    "eyes": {
        "total": 9995
    },
    "face": {
        "total": 9995
    },
    "fur": {
        "total": 9995
    },
    "hat": {
        "total": 9995
    }
}

def loadData(trait):
    obj = {}
    with open("./data/{0}.json".format(trait.name.lower())) as data:
        obj = json.loads(data.read())
    return obj

def generateJSON():
    dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
    for trait in Trait:
        if trait.name.lower() in dirs:
            with open("./data/{0}.json".format(trait.name.lower()), "w") as file:
                output = {}
                path = "./" + trait.name.lower()
                items = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                delimiters = ["background", "face", "fur", "eyes"]
                if not trait.name.lower() in delimiters:
                    print(trait.name.lower())
                    output["none"] = {
                        "url": "./misc/none.png",
                        "trait_type": trait.name.lower(),
                        "supply": 0,
                        "layer": trait.value
                    }
                for item in items:
                    # Layer exception for wings
                    layer = trait.value
                    if "wings" in item:
                        layer = trait.value - 1
                    output[item[:item.index(".png")]] = {
                        "url": "./" + trait.name.lower() + "/" + item,
                        "trait_type": trait.name.lower(),
                        "supply": 0,
                        "layer": layer 
                    }
                file.write(json.dumps(output))

def getMetadata(index, attributes):
    output = {
        "attributes": [],
        "description": "",
        "external_url": "https://happypandas.io",
        "image": "/ipfs/",
        "name": str(index)
    }
    for attr in attributes:
        output["attributes"] += [{
            "trait_type": attr["trait_type"],
            "value": attr["value"]
        }]
    return output

def generateImages():
    generateJSON()
    for _ in range(100):
        layers = []
        panda = Image.new(mode="RGBA", size=(2700, 2700), color=(255, 255, 255))
        # Generate list of attributes
        for trait in Trait:
            # Get trait JSON
            data = loadData(trait)
            # Random number 
            i = random.randint(0, len(list(data.keys())) - 1)
            # Random attribute
            attr = list(data.keys())[i]
            layers.append(data[attr])
        # Sort list ascending
        layers.sort(key=lambda x:x["layer"])
        # Iterate and swap if wings
        for i in range(len(layers)):
            if "wings" in layers[i]["url"]:
                layers[i-1]["layer"] += 1
        # Sort again
        layers.sort(key=lambda x:x["layer"])
        print(_, layers)
        # Create image
        for layer in layers:
            attr_img = Image.open(layer["url"]).convert("RGBA")
            panda.paste(attr_img, (0, 0), attr_img)
        panda = panda.convert("RGB")
        panda.save("./output/test_panda{0}.jpg".format(_))

def getSupply(trait, supply):
    data = loadData(trait)
    for item in data:
        data[item]['supply'] 
    print(data)
    pass

generateImages()
# getSupply(Trait.EYES)
# generateJSON()