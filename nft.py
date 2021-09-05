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
    FACE = 4
    CLOTHES = 5
    ACCESSORIES = 3
    HAT = 6
    
#  i = random.randint(0, len(list(hats.keys())) - 1)

def loadData(trait):
    obj = {}
    with open("./data/{0}.json".format(trait.name.lower())) as data:
        obj = json.loads(data.read())
    return obj

def getSupply(weights, max):
    if max == None:
        max = TOTAL_ITEMS
    total = sum(weights)
    supply = []
    for w in weights:
        supply += [int((w / total) * max)]
    # If supplies do not total properly, add 1 randomly
    if sum(supply) != TOTAL_ITEMS:
        i = random.randint(0, len(supply) - 1)
        supply[i] += 10000 - sum(supply)
    return supply

def getRarity(min, max, totalItems, curveType, stp):
    if curveType == "exp":
        # Solve for exponential function
        a = min
        b = max/min
        func = lambda x : min * (b**(stp * x))
        return [func(x / totalItems) for x in range(1, totalItems + 1)]
    elif curveType == "linear":
        m = max - min
        b = min
        return [(m * (x / totalItems)) + b for x in range(1, totalItems + 1)]
    else:
        return None

# weights = getRarity(0.65, 33, 23, "exp", 1)
# supply = getSupply(getRarity(0.65, 33, 23, "linear", 1))
# weights = [33, 4.7, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1, 2.9, 2.7, 2.5, 2.3, 2.1, 2.0, 1.8, 1.6, 1.4, 1.2, 1, 0.8, 0.6]
# supply = getSupply(weights, 6666)
# print(sum(supply))

# for _ in supply:
#     print(_)

def generateJSON():
    dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
    for trait in Trait:
        if trait.name.lower() in dirs:
            with open("./data/{0}.json".format(trait.name.lower()), "w") as file:
                output = {}
                path = "./" + trait.name.lower()
                items = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                output["none"] = {
                    "url": "./misc/none.png",
                    "trait_type": trait.name.lower(),
                    "weight": 0,
                    "supply": 0
                }
                for item in items:
                    output[item[:item.index(".png")]] = {
                        "url": "./" + trait.name.lower() + "/" + item,
                        "weight": 0,
                        "supply": 0
                    }
                file.write(json.dumps(output))

def generateImages():
    generateJSON()
    # load all trait data
    # generate supplies
    # paste routine
    dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
    for _ in range(100):
        panda = Image.new(mode="RGBA", size=(2700, 2700), color=(255, 255, 255))
        for trait in Trait:
            data = loadData(trait)
            if trait.name.lower() in dirs:
                # random attribute
                i = random.randint(0, len(list(data.keys())) - 1)

                keys = list(data.keys())
                attr = keys[i]

                # for i in range(len(keys)):
                #     if "scuba" in keys[i].lower():
                #         attr = keys[i]

                attr_img = Image.open(data[attr]["url"]).convert("RGBA")

                panda.paste(attr_img, (0, 0), attr_img)
        panda = panda.convert("RGB")
        panda.save("./output/test_panda{0}.jpg".format(_))

def setWeights():
    pass

generateImages()