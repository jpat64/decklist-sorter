from random import random
from math import floor
from requests import api
from time import sleep

class Card:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"{self.quantity} {self.name}"

def toMTGA(commander, deck, number):
    aboutPart = "About\n"
    spacingPart = "\n\n"
    commanderPart = "Commander\n"
    deckTitlePart = "Deck\n"
    deckPart = map(str, deck).join("\n")
    return f"{aboutPart}Player {number}'s Deck{spacingPart}{commanderPart}{commander}{spacingPart}{deckTitlePart}{deckPart}"
     

def main():
    deck = []
    added_cards = 0

    # first, pick a commander from a predetermined list
    valid_commander_names = [
        "Atogatog", 
        "Cromat", 
        "Marina Vendrell", 
        "Rukarumel, Biologist", 
        "Progenitus", 
        "Sliver Hivelord", 
        "Tom Bombadil",
        "Morophon, the Boundless", 
        "Reaper King", 
        "Ulalek, Fused Atrocity",
        "Surgeon General Commander", 
        "Tazri, Beacon of Unity"
    ]

    choice = valid_commander_names[floor(random() * len(valid_commander_names))]
    print("Added " + str(choice))
    commander = Card(name=choice, quantity=1)
    added_cards = 1

    base_url = "https://api.scryfall.com/cards/random"
    card_extension = "?q=-type%3Aland%20and%20f%3acommander"
    land_extension = "?q=type%3Aland%20and%20f%3acommander"

    while(added_cards < 62):
        response = api.get(f"{base_url}{card_extension}")       
        if response.status_code >= 400:
            print(f'bad response for random: {response.status_code}: {response.text}')
            return
        

        name = response.json()["name"]
        print("Added " + str(name))
        print("\t(Took " +str(response.elapsed) + "... time)")
        deck.append(Card(name=name, quantity=1))
        added_cards += 1
        sleep(0.1) # min. 100 milliseconds between requests
        
    
    while(added_cards < 85):
        response = api.get(f"{base_url}{land_extension}")       
        if response.status_code >= 400:
            print(f'bad response for random: {response.status_code}: {response.text}')
            return
        
        name = response.json()["name"]
        print("Added " + str(name))
        deck.append(Card(name=response.json()["name"], quantity=1))
        added_cards += 1
        sleep(0.1) # min. 100 milliseconds between requests
    
    deck.append(Card(name="Plains", quantity=3))
    deck.append(Card(name="Island", quantity=3))
    deck.append(Card(name="Swamp", quantity=3))
    deck.append(Card(name="Mountain", quantity=3))
    deck.append(Card(name="Forest", quantity=3))
    print("Added 3 of each basic land")
    
    print(toMTGA(commander=commander, deck=deck, number=1))

    
main()
