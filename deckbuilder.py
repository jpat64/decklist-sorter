from sys import argv
from decklist_reader import scrape_names
from scryfall_pinger import getScryfallInfo

def csvify(card_infos):
    toReturn = "Name, Color(s), Type, CMC, Quantity,\n"
    for info in card_infos:
        toReturn = toReturn + f'{info.card_name.replace(",", "")}, {info.card_color[0]}, {info.card_type}, {info.card_cost}, {str(info.quantities).replace(",", " --")}\n'
    return toReturn

    
def orderize_cards(filename):
    card_names = scrape_names(filename)

    card_infos = getScryfallInfo(card_names)

    card_infos.sort()

    return csvify(card_infos)

def main():
    if len(argv) < 2:
        print("usage: py deckbuilder.py [filename_of_cards.txt] [optional: filename_for_output.csv]")
        return
    
    cards = orderize_cards(argv[1])
    if (len(argv) == 3):
        outfile = open(argv[2], 'w')
        outfile.write(cards)
        print("wrote file: " + str(argv[2]))
    else: 
        print(cards)

main()

