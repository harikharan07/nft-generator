from PIL import Image
import random

"""
    draw from pool of 10000 attributes from each trait
    function to generate metadata for all 10000 images
"""

hats = {
    "trapper": {
        "url": "./hats/trapper.png",
        "supply": 0 
    },
    "scuba": {
        "url": "./hats/scuba.png",
        "supply": 0 
    },
    "cowboy": {
        "url": "./hats/cowboy.png",
        "supply": 0 
    },
    "astronaut": {
        "url": "./hats/astronaut.png",
        "supply": 0 
    }
}
# i = random.randint(0, len(list(hats.keys())) - 1)

def getRarity(min, max, totalItems, curveType):
    if curveType == "exp":
        # Solve for exponential function
        a = min
        b = max/min
        func = lambda x : min * (b**x)
        return [func(x / totalItems) for x in range(1, totalItems + 1)]
    elif curveType == "linear":
        m = max - min
        b = min
        return [(m * (x / totalItems)) + b for x in range(1, totalItems + 1)]
    else:
        return None

rarity = getRarity(0.5, 19, 12, "exp")

# for _ in rarity:
#     print(_)

for i in range(len(list(hats.keys()))):
    hat = list(hats.keys())[i]
    panda = Image.open("panda2.png")
    hat = Image.open(hats[hat]["url"])

    panda.paste(hat, (0, 0), hat)
    panda.save("test{0}.jpg".format(i))