from sys import argv

def scrape_names(filename):
    readfile = open(filename, 'r', encoding='utf-8')
    lines = readfile.readlines()
    #print(f'{filename} has {len(lines)} lines in it')
    deck_number = -1
    cards = [[]]
    index = 0
    do_not_read_cards = False
    for line in lines:
        words_separated = line.split(" ")
        # print(f'{words_separated}, {len(words_separated)}')
        if len(words_separated) > 1 and not do_not_read_cards:
            # not a category, like "Mainboard"
            index_of_first_space = line.index(" ")
            cardname = line[index_of_first_space + 1:-1]
            #print(f'reading card: {cardname}')
            # add the card once for each number before it- (i.e. "6 Plains" => "[Plains, Plains, Plains, Plains, Plains, Plains]")
            cards_to_add = [cardname] * int(words_separated[0])
            #print(f'deck number: {deck_number}')
            #print(f'cards: {cards}')
            if len(cards) == deck_number:
                cards.append([])
            cards[deck_number].extend(cards_to_add)
        elif words_separated[0][:-1] in ["Maybeboard", "Sideboard"]:
            #print(f'{index}: reading category, expecting Maybeboard or Sideboard: {words_separated[0]}')
            do_not_read_cards = True
        elif words_separated[0][:-1] in ["Mainboard"]:
            deck_number = deck_number + 1
            #print(f'{index}: reading category, expecting Mainboard: {words_separated[0][:-1]}, moving to deck {deck_number}')
            do_not_read_cards = False
        else:           
            #print(f'{index}: skipping: {words_separated}')
            continue
        index = index + 1
    return cards

"""
def main():
    # take in decklist filename
    if (len(argv) < 2) :
        print("usage: py decklist_reader.py [filename_of_decklist.txt]")
        return
    
    filename = argv[1]
    # spit out list of card names
    card_names = scrape_names(filename)
   #print(card_names)

main()
"""

