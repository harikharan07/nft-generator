import json

if __name__ == "__main__":
    for i in range(10000):
        output = {
            "attributes": [],
            "description": "",
            "external_url": "https://happypandas.io",
            "image": "ipfs://QmbG7E2Sk64Qr5DHwVt4Jqvr3acG8DcZfG6eAXESZKZgaf",
            "name": str(i)
        }
        file = open("./ipfs/{0}".format(i), "w+")
        file.write(json.dumps(output))
