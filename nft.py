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

def getSupply(weights):
    total = sum(weights)
    supply = []
    for w in weights:
        supply += [int((w / total) * TOTAL_ITEMS)]
    # If supplies do not total properly, add 1 randomly
    if sum(supply) != TOTAL_ITEMS:
        i = random.randint(0, len(supply) - 1)
        supply[i] += 1
    return supply

# for i in range(len(list(hats.keys()))):
#    hat = list(hats.keys())[i]
#    panda = Image.open("panda2.png")
#    hat = Image.open(hats[hat]["url"])

#    panda.paste(hat, (0, 0), hat)
#    panda.save("./output/test{0}.jpg".format(i))
