""" `microlib` is a script that implements a digital Zettelkasten.

author: fat_fox
creation date: 31-Aug-2021
last modified: 10-Feb-2021
"""
import argparse
import json
import os
from random import randrange


# Variables
symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
length = 20
with open('settings.json', 'r') as r:
    settings = json.load(r)


# Function implementations
def check_date(date: str, text: str) -> bool:
    """ Compares the date in the card with the specified date.
    """
    return date == text[:len(date)]


def check_number(number: str, text: str) -> bool:
    """ Compares the card number with the specified number.
    """
    return False if len(number) > len(text) else text[:len(number)] == number


def check_references(reference: str, text: str) -> bool:
    """ Checks if the specified reference is in the list of references in
        the index card.
    """
    return reference in text.split('/')


def check_words(words: str, text: str) -> bool:
    """ Checks if the specified words are in the index card.
    """
    return words.lower() in text.lower()


def find_card(args: argparse.Namespace) -> None:
    """ Searches for an index card using the specified arguments.
    """
    relevant_cards = []

    # Stop execution if there are no arguments
    if args.date == '' and args.number == '' and args.reference == '' and\
        args.words == '':
        print('No arguments!')
        return
    
    # Searching for cards in the current directory
    for file in os.listdir(settings['cards_path']):
        if os.path.splitext(file)[1] == '.txt':
            
            checks = [False] * 4
            checked = [False] * 4

            with open(os.path.join(settings['cards_path'], file), 'r',
                                                    encoding='utf-8') as f:
                # Reading the header of the file
                # Index card number
                current_number = f.readline().strip('\n') 
                if args.number.strip() != '':
                    checks[0] = check_number(args.number.strip(),
                                             current_number)
                    checked[0] = True

                # References
                if args.reference.strip() != '':
                    checks[1] = check_references(args.reference.strip(),
                                                 f.readline().strip('\n'))
                    checked[1] = True
                else:
                    f.readline()

                # Date
                if args.date.strip() != '':
                    checks[2] = check_date(args.date.strip(),
                                           f.readline().strip('\n'))
                    checked[2] = True
                else:
                    f.readline()

                # Reading the rest of the file
                if args.words.strip() != '':
                    text = " ".join([l.strip('\n') for l in f.readlines()
                                    if l.strip('\n') != ''])
                    checks[3] = check_words(args.words, text)
                    checked[3] = True

            # Accept or reject this card
            if True in checks and checks == checked:
                relevant_cards.append('{:<15} | {:<22}'.format(
                                                    current_number, file))

    print_card_list(relevant_cards)


def generate_name() -> str:
    """ Generates a name for the new index card.
    """
    new_name = ""

    while len(new_name) < length:
        new_name += symbols[randrange(0, len(symbols))-1]
    
    return new_name + '.txt'


def print_card_list(cl: list) -> None:
    """ Prints the specified list of index cards.
    """
    if len(cl) > 0:
        # Header
        print('{:<15} | {:<22}'.format('card number', 'card file'))
        print('-' * 49)
        # Body
        for card in sorted(cl): print(card)
    else:
        print('Nothing was found!')


# Main
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='`microlib v0.1` - searching'
        ' for an index card in the specified directory. To select the '
        'directory, modify the file `settings.json`')
    
    # Search arguments
    parser.add_argument('-n', dest='number', default='', type=str,
                        help='an index card number. Example: 1_111_a_2')
    parser.add_argument('-r', dest='reference', default='', type=str,
                        help='references in card. Example: 1_1/1_111_2/0')
    parser.add_argument('-d', dest='date', default='', type=str,
                        help='a creation date in the YYYYMMDD-format. '
                        'Example: 20210831')
    parser.add_argument('-w', dest='words', default='', type=str,
                        help='keywords. Example: INDEX')
    # Card manipulation arguments
    parser.add_argument('--generate', dest='generate',
                        action='store_true', help='generates a new card')
    parser.add_argument('--open', dest='open', default='', type=str,
                        help='opens the card specified by name. '
                        'Example: ./microlib -o <filename.txt>')
    parser.add_argument('--remove', dest='remove',
                        help='removes the index card '
                        'specified by name')
 
    args = parser.parse_args()

    if args.generate:
        new_name = generate_name()
        print("Creating the file: " +
                        os.path.join(settings['cards_path'], new_name))
        os.system(settings['editor'] + ' ' +
                        os.path.join(settings['cards_path'], new_name))
    elif args.open != '':
        os.system(settings['editor'] + ' ' +
                        os.path.join(settings['cards_path'], args.open))
    elif args.remove != '':
        os.remove(os.path.join(settings['cards_path'], args.remove))
    else:
        find_card(args)