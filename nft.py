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

TOTAL_ITEMS = 9995

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

    # Hashes of pandas
    hashes = []

    # Check supplies to ensure totals match
    for trait in TRAIT_SUPPLY:
        sum = 0
        for item in TRAIT_SUPPLY[trait]:
            if item != "total":
                sum += TRAIT_SUPPLY[trait][item]
        if sum != TOTAL_ITEMS:
            raise Exception("Supplies do not match totals")

    generateJSON()
    for _ in range(amount):
        layers = []
        panda = Image.new(mode="RGBA", size=(2700, 2700), color=(255, 255, 255))
        # Get possibilities
        # possibilities = 1
        # counts = []
        # for trait in Trait:
        #     total = 0
        #     for item in TRAIT_SUPPLY[trait.name.lower()]:
        #         if TRAIT_SUPPLY[trait.name.lower()][item] > 0:
        #             total += 1
        #     # Remove 'total' count
        #     total -= 1
        #     counts += [total]
        # for c in counts:
        #     possibilities = possibilities * c
        # print((_+1 / TOTAL_ITEMS) * 100)
        # print(possibilities)
        # Attributes list for metadata
        attributes = []
        # Generate list of attributes
        for trait in Trait:
            # Get trait JSON
            data = loadData(trait)
            # Create container for attribute
            attr = None
            # List of attributes with > 0 supply
            available = []
            for item in data:
                if TRAIT_SUPPLY[trait.name.lower()][item] > 0:
                    available.append(item)
            while(attr == None):
                # Random number 
                i = random.randint(0, len(available) - 1)
                # Random attribute
                temp = available[i]
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
        print(TRAIT_SUPPLY)
        # Pull metadata from layers
        metadata = getMetadata(_, attributes)
        f = open("./output/metadata/{0}.json".format(_), "w+")
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
        # Hash pandas
        # Separate trait names into new list and hash the list of strings
        # bc dict is not hashable
        # hashes += [hash(tuple(layers))]
        # Create image
        for layer in layers:
            attr_img = Image.open(layer["url"]).convert("RGBA")
            # panda.paste(attr_img, (0, 0), attr_img)
        # panda = panda.convert("RGB")
        # panda.save("./output/test_panda{0}.jpg".format(_))
    print(hashes)

def getSupply(trait, supply):
    data = loadData(trait)
    for item in data:
        data[item]['supply'] 
    pass

generateImages(9995)