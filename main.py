from pprint import pprint
import json

supply = [0.2500,0.0930,0.0850,0.0750,0.0650,0.0500,0.0480,0.0460,0.0440,0.0425,0.0415,0.0400,0.0350,0.0350,0.0300,0.0200,0.0155,0.0125,0.0111,0.0100,0.0050,0.0025,0.0015,0.0010]
value = ["Normal","Sunglasses","Stoned","Money","Glasses","3D Glasses","Designer Shades","Euro","Crying","Giant","BTC","Aderral","Reading Glasses","Eyepatch","Hypno Eyes","X-Techno Glasses","Red Albino Eyes","Black Eye","Aviators","Nightvision Goggles","ETH","Cyborg","Swim Goggles","SOL"]

if __name__ == "__main__":
    output = {}
    for i in range(len(value)):
        output[value[i]] = supply[i]
    print(json.dumps(output, indent=4, sort_keys=True))