import os
import re
import unicodedata

#current folders
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CARDS_DIRECTORY = SCRIPT_DIRECTORY + "/cards"
MTG_DIRECTORY = SCRIPT_DIRECTORY + "/cards/mtg"
LOCAL_DIRECTORY = SCRIPT_DIRECTORY + "/cards/local"
PRINT_DIRECTORY = SCRIPT_DIRECTORY + "/print/"

#basic lands list for exclusion
basic_lands = ["Plains", "Island", "Swamp", "Mountain", "Forest"]

#create cards folder if it doesn't exist
def create_cards_folder():
    if not os.path.exists(CARDS_DIRECTORY):
        os.mkdir(CARDS_DIRECTORY)
        os.mkdir(MTG_DIRECTORY)
        os.mkdir(LOCAL_DIRECTORY)
        print("Cards folder created")

def build_card_dictionary(card_list: str):
    card_dictionary = {}
    card_dictionary["total"] = 0

    if(len(card_list) > 0):
        for line in card_list.splitlines():
            if len(line) > 0:
                words = line.split(" ")
                #check if first word is an integer
                if words[0].isdigit():
                    #get card name
                    card_name = " ".join(words[1:])
                    
                    if(card_name not in basic_lands):
                        #get card number
                        card_number = words[0]
                        #add card to dictionary
                        card_dictionary[card_name] = int(card_number)
                        #update_total number of cards
                        card_dictionary["total"] += int(card_number)
                else:
                    #get card name
                    card_name = " ".join(words)
                    if(card_name not in basic_lands):
                        #add card to dictionary
                        card_dictionary[card_name] = 1
                        #update_total number of cards
                        card_dictionary["total"] += 1
                
    return card_dictionary
    
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
