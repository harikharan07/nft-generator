from pprint import pprint
import json

supply = [876,868,857,772,756,730,604,594,574,567,465,345,295,234,203,185,122,99,94,90,82,80,78,72,70,66,58,53,49,35,22]
value = ["Normal","Brown","Black","Orange","Blue","Gold","Bald","Rainbow","Shiny","Electric","Albino","Red","Zombie","Alien","Normal Tattoos","Shiny Tattoos","Zombie Tattoos","Robot Tattoos","Brown Tattoos","Orange Tattoos","Blue Tattoos","Red Tattoos","Gold Tattoos","Rainbow Tattoos","Bald Tattoos","Robot","Ghost","Alien Tattoos","Black Tattoos","Electric Tattoos","Albino Tattoos"]

if __name__ == "__main__":
    output = {}
    for i in range(len(value)):
        output[value[i]] = supply[i]
    print(json.dumps(output, indent=4, sort_keys=True))