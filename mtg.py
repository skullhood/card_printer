from time import sleep
from tkinter import StringVar
from util import *
import requests

SCRYFALL_TIMEOUT = .1

def download_card_image(card_faces):
    if(card_faces["num_faces"] == 1):
        print(card_faces)
        response = requests.get(card_faces["faces"][0]['uri'])
        
        card_folder = MTG_DIRECTORY + "/" + card_faces["faces"][0]['name']

        image_file = card_folder + "/card.png"

        if not os.path.exists(card_folder):
            os.mkdir(card_folder)

        if response.status_code == 200:
            with open(image_file , "wb") as f:
                f.write(response.content)
        else:
            print("STATUS {} Something went wrong while downloading the card image!", response.status_code)
    elif(card_faces["num_faces"] > 1):
        card_folders = []
        card_count = 1
        for face in card_faces["faces"]:            
            print(face)
            card_folder = MTG_DIRECTORY + "/" + face['name']
            if not os.path.exists(card_folder):
                os.mkdir(card_folder)
                card_folders.append(card_folder)
        for face in card_faces["faces"]:
            response = requests.get(face['uri'])
            if response.status_code == 200:
                for card_folder in card_folders:
                    image_file = card_folder + "/card{}.png".format(card_count)
                    with open(image_file , "wb") as f:
                        f.write(response.content)
            else:
                print("STATUS {} Something went wrong while downloading the card image!", response.status_code)
            card_count = card_count + 1

def download_card_object(card_name: str):
    url = "https://api.scryfall.com/cards/named?fuzzy=" + card_name
    response = requests.get(url)

    if response.status_code == 200:
        card_object = response.json()
        
        card_faces = {"num_faces": 0, "faces": []}

        if "image_uris" in card_object:
            png = card_object["image_uris"]["png"]
            if png != None:
                sleep(SCRYFALL_TIMEOUT)
                card_faces["num_faces"] = 1
                card_faces["faces"].append({
                    "name": card_name,
                    "uri": png
                })
                download_card_image(card_faces)
        elif "card_faces" in card_object: 
            for face in card_object["card_faces"]:
                print("faces")
                if "image_uris" in face:
                    print("uris")
                    png = face["image_uris"]["png"]
                    if png != None:
                        print("png")
                        sleep(SCRYFALL_TIMEOUT)
                        card_faces["num_faces"] = card_faces["num_faces"] + 1
                        card_faces["faces"].append({
                            "name": slugify(face['name']),
                            "uri": png
                        })
            download_card_image(card_faces)
        else:
            print("NO IMAGE URL FOR CARD: " + card_name)
    else:
        print("STATUS {} Something went wrong while getting the card object!", response.status_code)

def download_cards_not_downloaded(card_dictionary: dict, processing_status_var: StringVar):
    for card_name in card_dictionary:
        if card_name != "total":
            card_name = slugify(card_name)
            if not os.path.exists(MTG_DIRECTORY + "/" + card_name):
                processing_status_var.set("Downloading " + card_name + "...")
                download_card_object(card_name)
                sleep(SCRYFALL_TIMEOUT)
                processing_status_var.set("Downloaded " + card_name + "!")