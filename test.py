import random
import json
from os import listdir, rename
from os.path import isfile, join

onlyfiles = [f for f in listdir("./output/metadata") if isfile(join("./output/metadata", f))]
path = "./output/metadata/"
i = 0
for file in onlyfiles:
    with open(path + file, "r") as metadata:
        data = json.loads(metadata.read())
        obj = {
            "name": "Frog #" + str(i),
            "symbol": "FROG",
            "description": "The frogs are having a party!",
            "image": "https://ipfs.io/ipfs/QmXxoLZYdzw5as8cFeNnrSXiGQoazDZ74vwyyezYynQgM6/{0}.png/".format(i),
            "seller_fee_basis_points": 200,
            "external_url": "frog-party.io",
            "attributes": data["attributes"],
            "collection": {
                "name": "Frog Party"
            },
            "properties": {
                "files": [
                    {
                        "uri": "https://ipfs.io/ipfs/QmXxoLZYdzw5as8cFeNnrSXiGQoazDZ74vwyyezYynQgM6/{0}.png/".format(i),
                        "type": "image/png"
                    }
                ],
                "creators": [
                    {
                        "address": "CMetYfSiXPBWB8pXGYyJK3ThFpk2pvNxixJTE4aEXCq3",
                        "share": 100
                    }
                ]
            }
        }
        file = open("./newdata/" + str(i), "w")
        file.write(json.dumps(obj))
        i += 1