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

# Get rarity stats for generated set
def getStatistics():
    # Store appearances of traits
    traitDict = {}
    # Path to metadata
    path = "./output/metadata/"
    items = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for i in range(len(items)):
        index = int(items[i][:items[i].index(".json")])
        with open(path + items[i]) as file:
            data = json.loads(file.read())
            for trait in data["attributes"]:
                if trait["trait_type"] in traitDict:
                    if trait["value"] in traitDict[trait["trait_type"]]:
                        traitDict[trait["trait_type"]][trait["value"]] += 1
                    else:
                        traitDict[trait["trait_type"]][trait["value"]] = 1
                else:
                    traitDict[trait["trait_type"]] = {}
    return traitDict

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

def getAttributes(hashes):
    global TRAIT_SUPPLY
    while True:
        def select(values):
            variate = random.random() * sum(values.values())
            cumulative = 0.0
            for item, weight in values.items():
                cumulative += weight
                if variate < cumulative:
                    return item
            return item # Shouldn't get here, but just in case of rounding...

        attributes = []
        for trait in Trait:
            attr = select(TRAIT_SUPPLY[trait.name.lower()])
            attributes += [attr]
        if not hash(tuple(attributes)) in hashes:
            break
    return attributes

def getRandomAttributes(hashes):
    global TRAIT_SUPPLY
    while True:
        def select(trait):
            keys = list(TRAIT_SUPPLY[trait])
            i = random.randint(0, len(keys) - 1)
            return keys[i]

        attributes = []
        for trait in Trait:
            attr = select(trait.name.lower())
            attributes += [attr]

        if not hash(tuple(attributes)) in hashes:
            break
    return attributes

def generateImages(amount):
    global TRAIT_SUPPLY
    # Hashes of pandas
    hashes = {}
    # Check supplies to ensure totals match
    for trait in TRAIT_SUPPLY:
        s = 0
        for item in TRAIT_SUPPLY[trait]:
            if item != "total":
                s += TRAIT_SUPPLY[trait][item]
        if s != TOTAL_ITEMS:
            raise Exception("Supplies do not match totals")

    generateJSON()
    for _ in range(0, amount):
        layers = []
        panda = Image.new(mode="RGBA", size=(2700, 2700), color=(255, 255, 255))
        # Attributes list for metadata
        attributes = getRandomAttributes(hashes)
        # Attribute metadata output
        output = []
        for i in range(len(attributes)):
            trait = Trait(i)
            data = loadData(trait)
            # Add attributes to metadata list
            output += [{
                "trait_type": trait.name.lower(),
                "value": attributes[i]
            }]
            layers.append(data[attributes[i]])
        # Pull metadata from layers
        metadata = getMetadata(_, output)
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
        # Sort again
        layers.sort(key=lambda x:x["layer"])
        # Hash pandas
        pandaHash = hash(tuple(map(lambda x:x["url"][2:].replace('.png','')[x["url"][2:].index('/')+1:], layers)))
        if pandaHash in hashes:
            print(_)
            print(layers)
            hashes[pandaHash] += 1
        else:
            hashes[pandaHash] = 0
        # Create image
        for layer in layers:
            attr_img = Image.open(layer["url"]).convert("RGBA")
            panda.paste(attr_img, (0, 0), attr_img)
        panda = panda.convert("RGB")
        panda.save("./output/test_panda{0}.jpg".format(_))
        print("Progress:", (_ / 9995) * 100)
    same = 0
    for h in hashes:
        if hashes[h] > 0:
            same += 1
    print("Identical Pandas", same)

# generateImages(9995)
getStatistics()