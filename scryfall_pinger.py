from requests import api
from sys import argv
import json
import time
from decklist_reader import scrape_names
import functools


    

cardcolors = {
    "W": ("White", 1),
    "U":("Blue",  2),
    "B":("Black", 3),
    "R":("Red",  4),
    "G":("Green",  5),
    "C":("Colorless", 6),
    "WU":("Azorius",  7),
    "WB":("Orzhov",  8),
    "WR":("Boros", 9),
    "WG":("Selesnya",  10),
    "UB":("Dimir",  11),
    "UR":("Izzet", 12),
    "UG":("Simic",  13),
    "BR":("Rakdos", 14),
    "BG":("Golgari",  15),
    "RG":("Gruul", 16),
    "WBG":("Abzan", 17),
    "WUG":("Bant", 18),
    "WUB":("Esper", 19),
    "UBR":("Grixis", 20),
    "WUR":("Jeskai", 21),
    "BRG":("Jund", 22),
    "WBR":("Mardu", 23),
    "WRG":("Naya", 24),
    "UBG":("Sultai", 25),
    "URG":("Temur", 26),
    "UBRG":("Glint-Eye", 27),
    "WUBG":("Witch-Maw", 27),
    "WURG":("Ink-Treader", 27),
    "WBRG":("Dune-Brood", 27),
    "WUBR":("Yore-Tiller", 27),
    "WUBRG":("Rainbow", 27),
    "X":("Unaffiliated", 28),
}
type_hierarchies = {"Creature":0, "Permanent":1, "Instant":2, "Sorcery":3, "NA":4, "Not Mana Rock":5, "Mana Rock":6, "Land":7, "Basic":8}
cost_hierarchies = {"0-1":0, "2":1, "3":2,"4":3,"5":4,"6+":5}

@functools.total_ordering
class CardInfo:
    def __init__(self, card_name, card_color, card_type, card_cost, quantities):
        self.card_name = card_name
        self.card_color = card_color
        self.card_type = card_type
        self.card_cost = card_cost
        self.quantities = quantities

    def __repr__(self):
        return f'{self.card_name}, {self.card_color}, {self.card_type}, {self.card_cost}, {str(self.quantities).replace(",", " --")}'
    
    def __eq__(self, other):
        return self.card_name.strip() == other.card_name.strip()
    
    def __lt__(self, other):
        # first, by color
        if self.card_color[1] != other.card_color[1]:
            return self.card_color[1] < other.card_color[1]
        # next, by type
        elif type_hierarchies[self.card_type] != type_hierarchies[other.card_type]:
            return type_hierarchies[self.card_type] < type_hierarchies[other.card_type]
        # next, by cost
        elif cost_hierarchies[self.card_cost] != cost_hierarchies[other.card_cost]:
            return cost_hierarchies[self.card_cost] < cost_hierarchies[other.card_cost]
        # finally, by name
        return self.card_name.strip() < other.card_name.strip()
            

def getScryfallInfo(card_list):
    cards = []
    deck_number = 0
    #print("decks found:" + str(len(card_list)))
    for deck in card_list:
        for card in deck:
            time.sleep(0.1) # min. 100 milliseconds between requests
            response = api.get("https://api.scryfall.com/cards/search", params={"q":f'!\"{card}\"'})
            if response.status_code >= 400:
                print(f'bad response for {card}: {response.status_code}: {response.text}')
                exit
            
            data = response.json()["data"][0]
            card = parseCard(data)
            card.quantities[deck_number] = 1
            try: 
                card_index = cards.index(card)
                try: 
                    how_many_of_this_card_is_in_the_deck_already = cards[card_index].quantities[deck_number]
                except: 
                    how_many_of_this_card_is_in_the_deck_already = 0
                if how_many_of_this_card_is_in_the_deck_already > 0:
                    cards[card_index].quantities[deck_number] = how_many_of_this_card_is_in_the_deck_already + 1
                else:
                    cards[card_index].quantities[deck_number] = 1
            except:
                cards.append(card)
            continue
        deck_number = deck_number + 1
    return cards

def parseCard(card_info):
    #print(card_info)
    colors = parseColors(card_info=card_info)
    card_type = parseType(card_info=card_info, colors=colors)
    return CardInfo(
        card_name=card_info["name"],
        card_color=colors,
        card_type=card_type,
        card_cost=parseCost(card_info=card_info),
        quantities={}
    )   

def condense_color_id(color_identity):
    toReturn = ""
    if "W" in color_identity:
        toReturn = toReturn + "W"
    if "U" in color_identity:
        toReturn = toReturn + "U"
    if "B" in color_identity:
        toReturn = toReturn + "B"
    if "R" in color_identity:
        toReturn = toReturn + "R"
    if "G" in color_identity:
        toReturn = toReturn + "G"
    if len(toReturn) == 0:
        toReturn = "C"
    return toReturn

def parseColors(card_info):
    color_identity = card_info["color_identity"]
    return cardcolors[condense_color_id(color_identity=color_identity)]

def condense(proper_type):
    if proper_type in ["Enchantment", "Artifact", "Planeswalker", "Battle"]:
        return "Permanent"
    return proper_type

def parseType(card_info, colors):
    # if colors > 1, return "Land" or "NA"
    if colors[1] > 6:
        try:
            type_line = card_info["type_line"]
        except:
            type_line = card_info["card_faces"][0]["type_line"]
        if "Land" in type_line:
            return "Land"
        else:
            return "NA"
    
    # if colorless, discern if it's a mana rock (card text contains "{T}: Add")
    if colors[1] == 6:
        try:
            oracle_text = card_info["oracle_text"]
            type_line = card_info["type_line"]
        except:
            oracle_text = card_info["card_faces"][0]["oracle_text"]
            type_line = card_info["card_faces"][0]["type_line"]
        if "Basic" in type_line and "Snow" not in type_line:
            return "Basic"
        elif "Land" in type_line:
            return "Land"
        elif "{T}: Add" in oracle_text:
            return "Mana Rock"
        else:
            return "Not Mana Rock"
    
    # if monocolor, see if it's a split card or an mdfc
    # hierarchy: land > creature > permanent > sorcery > instant
    normal_hierarchy = ["Land", "Creature", "Enchantment", "Artifact", "Planeswalker", "Battle", "Sorcery", "Instant"]
    mdfc_hierarchy = ["Creature", "Enchantment", "Artifact", "Planeswalker", "Battle", "Sorcery", "Instant", "Land"]
    card_type = card_info["layout"]
    type_line = card_info["type_line"]
    # treat all mdfcs as their non-land type
    if card_type == "modal_dfc":
        for i in range(len(mdfc_hierarchy)):
            if mdfc_hierarchy[i] in type_line:
                return condense(mdfc_hierarchy[i])
    else:
        for i in range(len(mdfc_hierarchy)):
            if normal_hierarchy[i] in type_line:
                return condense(normal_hierarchy[i])
            
# the implementation of this is confusing, so hopefully these examples help explain it            
# {W}{W} ? num_symbols = 2 good!
# {1}{W}{W} ? num_symbols = 3 good!
# {2}{W}{W} ? num_symbols = 3 bad!
# {0} ? num_symbols = 1 bad!
# if generic_cost is not 1, then we need to take it into account -> num_symbols - 1 + generic_cost
# if generic_cost is 1, then we just need num_symbols -> num_symbols - 1 + 1
# if there is no generic_cost, then we just need num_symbols -> num_symbols (so set generic_cost to 1 and use same formula)
def count_pips_and_add_colorless(mana_cost):
    num_symbols = mana_cost.count("{")
    try:
        generic_cost = int(mana_cost[1])
    except:
        generic_cost = 1
    return num_symbols - 1 + generic_cost
    

def parseCost(card_info):
    # only care about the "front" side- the side that comes before the //
    front_side_name = card_info["name"].split("//")[0]
    #print(card_info["name"] + " " + card_info["layout"])
    try: 
        card_faces = card_info["card_faces"]
    except:
        card_faces = []

    if len(card_faces) == 0:
        card_data = card_info
    else:
        card_faces = card_info["card_faces"]
        card_data = card_faces[0] if card_faces[0]["name"] in front_side_name else card_faces[1]
    #print(f'choosing {card_data["name"]} from {card_info["name"]}')
    #print(f'mana cost: {card_data["mana_cost"]}')
    mana_cost = card_data["mana_cost"]
    if len(mana_cost) == 0:
        return "0-1"
    if "{X}" in mana_cost:
        return "6+"
    calculated_mana_cost = count_pips_and_add_colorless(mana_cost)
    if calculated_mana_cost <= 1:
        return "0-1"
    elif calculated_mana_cost >= 6:
        return "6+"
    else:
        return str(calculated_mana_cost)

"""   
def main():
    if len(argv) < 2:
        print("usage: py scryfall_pinger.py  [card name]")
        return
    
    cards = getScryfallInfo(scrape_names(argv[1]))
    for card in cards:
       #print(repr(card) + "\n")
       continue

main()
"""