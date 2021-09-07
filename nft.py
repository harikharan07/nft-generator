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

TOTAL_ITEMS = 9900

class Trait(Enum):
    BACKGROUND = 0
    FUR = 1
    EYES = 2
    CLOTHES = 3
    ACCESSORIES = 4
    FACE = 5
    HEAD = 6

# Load trait data
f = open("./data/supply.json", "r")
TRAIT_SUPPLY = json.loads(f.read())

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
                    output["none"] = {
                        "url": "./misc/none.png",
                        "trait_type": trait.name.lower(),
                        "layer": trait.value
                    }
                for item in items:
                    # Layer exception for wings
                    layer = trait.value
                    if "wings" in item.lower():
                        layer = trait.value - 1
                    output[item[:item.index(".png")]] = {
                        "url": "./" + trait.name.lower() + "/" + item,
                        "trait_type": trait.name.lower(),
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

def generateImages(amount):
    global TRAIT_SUPPLY
    generateJSON()
    for _ in range(amount):
        layers = []
        panda = Image.new(mode="RGBA", size=(2700, 2700), color=(255, 255, 255))
        # Attributes list for metadata
        attributes = []
        # Generate list of attributes
        for trait in Trait:
            # Get trait JSON
            data = loadData(trait)
            # Create container for attribute
            attr = None
            while(attr == None):
                # Random number 
                i = random.randint(0, len(list(data.keys())) - 1)
                # Random attribute
                temp = list(data.keys())[i]
                # If there is supply assign attr
                if TRAIT_SUPPLY[trait.name.lower()][temp] > 0:
                    attr = temp
            # Decrement supply
            TRAIT_SUPPLY[trait.name.lower()]["total"] -= 1
            TRAIT_SUPPLY[trait.name.lower()][attr] -= 1
            # Add attributes to metadata list
            attributes += [{
                "trait_type": trait.name.lower(),
                "value": attr
            }]
            layers.append(data[attr])
        # Pull metadata from layers
        metadata = getMetadata(_, attributes)
        f = open("./output/metadata/data.json", "w+")
        f.write(json.dumps(metadata))
        f.close()
        # Sort list ascending
        layers.sort(key=lambda x:x["layer"])
        # Iterate and swap if wings
        for i in range(len(layers)):
            # If wings, swap layers
            if "wings" in layers[i]["url"].lower():
                layers[i-1]["layer"] += 1
                print(layers[i-1])
        # Sort again
        layers.sort(key=lambda x:x["layer"])
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

generateImages(9995)