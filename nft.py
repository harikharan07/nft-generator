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
    HAT = 1
    EYES = 2
    FUR = 3
    FACE = 4
    CLOTHES = 5
    
#  i = random.randint(0, len(list(hats.keys())) - 1)

def loadData():
    obj = {}
    for trait in Trait:
        with open("./data/{0}.json".format(trait.name.lower())) as data:
            obj[trait.name.lower()] = json.loads(data.read())
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

weights = getRarity(0.65, 33, 23, "exp", 1)
# supply = getSupply(getRarity(0.65, 33, 23, "linear", 1))
# weights = [33, 4.7, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1, 2.9, 2.7, 2.5, 2.3, 2.1, 2.0, 1.8, 1.6, 1.4, 1.2, 1, 0.8, 0.6]
supply = getSupply(weights, 6666)
# print(sum(supply))

for _ in supply:
    print(_)

# for i in range(len(list(hats.keys()))):
#    hat = list(hats.keys())[i]
#    panda = Image.open("panda2.png")
#    hat = Image.open(hats[hat]["url"])
def generateImages():
    BASE = "panda2.png"
    # load all trait data
    # generate supplies
    # paste routine
    for trait in Trait:
        data = loadData(trait)

        for i in range(len(list(data.keys()))):
            attr = list(data.keys())[i]
            panda = Image.open(BASE)
            attr_img = Image.open(data[attr]["url"])

            panda.paste(attr_img, (0, 0), attr_img)
            panda.save("./output/test_panda{0}.jpg".format(i))
