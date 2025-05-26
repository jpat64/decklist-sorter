from random import random
from math import floor
from requests import api
from time import sleep
import json

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
    deckPart = str.join("\n", list(map(str, deck)))
    return f"{aboutPart}Player {number}'s Deck{spacingPart}{commanderPart}{commander}{spacingPart}{deckTitlePart}{deckPart}"
     

def main():
    deck = []
    added_cards = 0

    if True:
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

        cards = open("default-cards.json", 'r', encoding='utf-8')
        
        json_of_cards = json.load(cards)

        excluded_card_names = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
        excluded_card_names.append(choice)

        while (added_cards < 85):
            random_card = json_of_cards[floor(random() * len(json_of_cards))]
            name = random_card["name"]
            legal = random_card["legalities"]["commander"] == "legal"
            if legal and (name not in excluded_card_names):
                quantity = 1
                deck.append(Card(name=name, quantity=quantity))
                excluded_card_names.append(name)
                added_cards += 1
                print(f"Added {name}")
            else:
                print(f"Did not add {name} because it was either not legal or we already have one")
        
        deck.append(Card(name="Plains", quantity=2))
        deck.append(Card(name="Island", quantity=2))
        deck.append(Card(name="Swamp", quantity=2))
        deck.append(Card(name="Mountain", quantity=2))
        deck.append(Card(name="Forest", quantity=2))
        deck.append(Card(name="Snow-Covered Plains", quantity=1))
        deck.append(Card(name="Snow-Covered Island", quantity=1))
        deck.append(Card(name="Snow-Covered Swamp", quantity=1))
        deck.append(Card(name="Snow-Covered Mountain", quantity=1))
        deck.append(Card(name="Snow-Covered Forest", quantity=1))

        cards.close()

        writefile = open("bracket_zero_list_1.txt", "w")
        writefile.write(toMTGA(commander, deck, 1))

    
main()
